import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
from ..client import (
    query_traffic_volume, TrafficVolume, VolumeByHour,
    query_traffic_volume_by_day, DailyTrafficVolume, VolumeByDay,
    create_timeseries_df
)

# Test constants
INVALID_URL = "https://invalid-url-that-does-not-exist.com/"
INVALID_POINT_ID = "invalid_point_id"
BASE_URL = "https://trafikkdata-api.atlas.vegvesen.no/"
TEST_POINT_ID = "97411V72313"  # E6 Mortenhals

def test_pagination_byHour():
    """Test that pagination works correctly for hourly data over multiple days"""
    # Request 3 days of data (72 hours, should require pagination as limit is 100)
    end_time = datetime.now(ZoneInfo("Europe/Oslo")).replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=3)
    
    result = query_traffic_volume(
        BASE_URL,
        TEST_POINT_ID,
        start_time.astimezone(ZoneInfo("Europe/Oslo")).isoformat(),
        end_time.astimezone(ZoneInfo("Europe/Oslo")).isoformat()
    )
    
    assert isinstance(result, TrafficVolume)
    assert result.point_id == TEST_POINT_ID
    assert len(result.volumes) >= 70  # Should have ~72 hours of data
    
    # Verify chronological order and no gaps
    for i in range(len(result.volumes) - 1):
        current = result.volumes[i]
        next_vol = result.volumes[i + 1]
        assert current.to_time == next_vol.from_time
        assert isinstance(current.total, int)
        assert 0 <= current.coverage_percentage <= 100

def test_single_page_byHour():
    """Test fetching data that fits in a single page"""
    # Request 12 hours of data (should fit in one page)
    end_time = datetime.now(ZoneInfo("Europe/Oslo")).replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=12)
    
    result = query_traffic_volume(
        BASE_URL,
        TEST_POINT_ID,
        start_time.isoformat(),
        end_time.isoformat()
    )
    
    assert isinstance(result, TrafficVolume)
    assert len(result.volumes) <= 12
    assert all(isinstance(v, VolumeByHour) for v in result.volumes)
    
    # Verify timezone information is preserved
    for volume in result.volumes:
        assert volume.from_time.tzinfo is not None
        assert volume.to_time.tzinfo is not None
        # Accept both named timezones and offset format
        tz_name = volume.from_time.tzname()
        assert any(name in tz_name for name in ["CET", "CEST", "UTC+01:00", "UTC+02:00"])

def test_invalid_url():
    """Test that invalid URL raises appropriate exception"""
    with pytest.raises(Exception) as exc_info:
        query_traffic_volume(
            INVALID_URL,
            TEST_POINT_ID,
            datetime.now(ZoneInfo("Europe/Oslo")).isoformat(),
            datetime.now(ZoneInfo("Europe/Oslo")).isoformat()
        )
    # Connection errors are also valid for invalid URLs
    error_msg = str(exc_info.value)
    assert any(msg in error_msg for msg in ["Query failed", "Max retries exceeded", "Failed to resolve"])

def test_invalid_point_id():
    """Test that invalid point ID results in GraphQL error"""
    with pytest.raises(Exception) as exc_info:
        query_traffic_volume(
            BASE_URL,
            INVALID_POINT_ID,
            datetime.now(ZoneInfo("Europe/Oslo")).isoformat(),
            datetime.now(ZoneInfo("Europe/Oslo")).isoformat()
        )
    assert "GraphQL errors" in str(exc_info.value)

def test_daily_volume():
    """Test fetching daily traffic volume data"""
    # Request 7 days of data
    end_time = datetime.now(ZoneInfo("Europe/Oslo")).replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)
    
    result = query_traffic_volume_by_day(
        BASE_URL,
        TEST_POINT_ID,
        start_time.isoformat(),
        end_time.isoformat()
    )
    
    assert isinstance(result, DailyTrafficVolume)
    assert result.point_id == TEST_POINT_ID
    assert len(result.volumes) <= 7  # Should have up to 7 days of data
    
    # Verify data structure and values
    for volume in result.volumes:
        assert isinstance(volume, VolumeByDay)
        assert isinstance(volume.total, int)
        assert 0 <= volume.coverage_percentage <= 100
        assert volume.from_time.tzinfo is not None
        assert volume.to_time.tzinfo is not None
        # Verify each period is exactly 24 hours
        assert (volume.to_time - volume.from_time).total_seconds() == 24 * 60 * 60

def test_invalid_date_range():
    """Test that end time before start time raises error"""
    end_time = datetime.now(ZoneInfo("Europe/Oslo"))
    start_time = end_time + timedelta(days=1)  # Start time after end time
    
    with pytest.raises(Exception) as exc_info:
        query_traffic_volume(
            BASE_URL,
            TEST_POINT_ID,
            start_time.isoformat(),
            end_time.isoformat()
        )
    assert "GraphQL errors" in str(exc_info.value)

def test_create_timeseries_df():
    """Test creating a DataFrame with multiple points"""
    # Set up test data with explicit timezone handling
    oslo_tz = ZoneInfo("Europe/Oslo")
    now = datetime.now(oslo_tz)
    end_time = now.replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=24)
    # Convert times to Oslo timezone
    end_time = end_time.astimezone(oslo_tz)
    start_time = start_time.astimezone(oslo_tz)
    point_ids = [TEST_POINT_ID, "65271V443150"]  # Two real points: E6 Mortenhals and another valid point
    
    # Create DataFrame with explicit timezone offset in ISO format
    df = create_timeseries_df(
        BASE_URL,
        point_ids,
        start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        end_time.strftime("%Y-%m-%dT%H:%M:%S")
    )
    
    # Verify DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert all(point_id in df.columns for point_id in point_ids)
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.freq == 'h'
    assert df.index.tz is not None
    
    # Verify data
    assert not df.empty
    assert df.index[0].tz == oslo_tz
        
    # Print actual dtypes for debugging
    print("\nActual column dtypes:")
    print(df.dtypes)
        
    # Check each column's dtype individually
    for col in df.columns:
        assert df[col].dtype == 'Int64', f"Column {col} has dtype {df[col].dtype}, expected Int64"
    assert all(df[col].notna().any() for col in df.columns)  # At least some data per column

def test_create_timeseries_df_invalid_point():
    """Test DataFrame creation with an invalid point ID"""
    # Set up test data with explicit timezone handling
    oslo_tz = ZoneInfo("Europe/Oslo")
    now = datetime.now(oslo_tz)
    end_time = now.replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(hours=24)
    # Convert times to Oslo timezone
    end_time = end_time.astimezone(oslo_tz)
    start_time = start_time.astimezone(oslo_tz)
    point_ids = [TEST_POINT_ID, "invalid_point_id"]
    
    # Should still create DataFrame but with NaN for invalid point
    df = create_timeseries_df(
        BASE_URL,
        point_ids,
        start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        end_time.strftime("%Y-%m-%dT%H:%M:%S")
    )
    
    assert isinstance(df, pd.DataFrame)
    assert "invalid_point_id" in df.columns
    assert df["invalid_point_id"].isna().all()  # All values should be NaN
    assert not df[TEST_POINT_ID].isna().all()  # Valid point should have data
