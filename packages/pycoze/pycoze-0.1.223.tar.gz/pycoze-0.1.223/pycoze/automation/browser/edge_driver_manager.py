import os
import requests
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver


# Function to check network availability
def is_network_available():
    try:
        # Attempt to access the download URL for Edge Chromium driver to check network connection
        response = requests.get("https://msedgedriver.azureedge.net/", timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


# Function to get the default download path for Edge Chromium driver
def get_default_driver_path():
    manager = EdgeChromiumDriverManager()
    return manager.install()


# Function to get the driver version from cache
def get_cached_driver_version(manager):
    cache_dir = manager._cache_manager._root_dir  # Get the root path of the cache directory
    os_type = manager._os_system_manager.get_os_type()  # Get the OS type
    driver_name = manager.driver.get_name()

    # List all versions in the cache directory
    versions_dir = os.path.join(cache_dir, "drivers", driver_name, os_type)
    if os.path.exists(versions_dir):
        versions = os.listdir(versions_dir)
        if versions:
            # Return the latest version found in the cache
            return max(versions)
    return None


# Function to check if the driver has already been downloaded
def get_driver_path():
    network_available = is_network_available()
    print("Network status:", "Available" if network_available else "Unavailable")
    manager = EdgeChromiumDriverManager()
    if network_available:
        return get_default_driver_path()
    else:
        # If no network, check the cache directory
        driver_version = get_cached_driver_version(manager)
        if driver_version:
            driver_name = manager.driver.get_name()
            os_type = manager._os_system_manager.get_os_type()
            cache_dir = manager._cache_manager._root_dir

            # Determine the correct driver filename based on the OS
            if os.name == 'nt':  # Windows
                driver_filename = "msedgedriver.exe"
            else:  # macOS and Linux
                driver_filename = "msedgedriver"

            # Construct the driver path
            driver_path = os.path.join(cache_dir, "drivers", driver_name, os_type, driver_version, driver_filename)
            # Check if the driver path exists
            if os.path.exists(driver_path):
                return driver_path
        raise Exception("Network unavailable and no downloaded driver found")


# Function to get the Edge driver service
def get_edge_driver_service():
    driver_path = get_driver_path()
    print("driver_path", driver_path)
    # Check if the driver path exists
    if os.path.exists(driver_path):
        return Service(driver_path)
    else:
        raise Exception("Network unavailable and no downloaded driver found")