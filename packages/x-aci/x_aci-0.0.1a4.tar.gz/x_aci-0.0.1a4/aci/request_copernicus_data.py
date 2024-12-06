#!/usr/bin/env python3
import os
import subprocess
import cdsapi


class Era5var:
    """
    This class contains methods for extracting ERA5 data.

    Attributes:
        area (str): Name of the area for which data is required (e.g., 'France', 'London').
        coordinates (list): List of north, west, south, and east coordinates that bound the area.
        years (str): Beginning and end year for extraction separated by a dash (e.g., '1961-1963') or a
        single year (e.g., '1961').
        variable_name (str): Name of the variable to extract (e.g., 'total_precipitation').
        monthly (bool): If True, the extraction will be done month by month and then merged (useful for large data).
    """

    def __init__(self, area, coordinates, years, variable_name, monthly=None):
        """
        Initializes the Era5var object with the specified parameters.

        Args:
            area (str): Name of the area.
            coordinates (list): Coordinates bounding the area.
            years (str): Year range for extraction.
            variable_name (str): Variable name to extract.
            monthly (bool, optional): Whether to extract data month by month. Defaults to None.
        """
        if len(years) == 9:  # Format 'YYYY-YYYY'
            self.years_included = [str(year) for year in range(int(years[:4]), int(years[5:]) + 1)]
        elif len(years) == 4:  # Format 'YYYY'
            self.years_included = [years]
        else:
            raise ValueError("years in wrong format")

        self.area_name = area
        self.coordinates = coordinates
        self.variable_name = variable_name
        self.monthly = False if monthly is None else monthly

    def request_data(self):
        """
        Requests the ERA5 data based on the initialization parameters.
        """
        directory = "../data/data0"
        # Create directory if it does not exist
        if not os.path.exists(directory):
            try:
                subprocess.run(["mkdir", directory], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error creating directory: {e}")

        c = cdsapi.Client()

        if not self.monthly:
            # Single request for the entire period
            for year in self.years_included:
                c.retrieve(
                    'reanalysis-era5-single-levels',
                    {
                        'product_type': 'reanalysis',
                        'variable': self.variable_name,
                        'year': year,
                        'month': [f'{month:02d}' for month in range(1, 13)],
                        'day': [f'{day:02d}' for day in range(1, 32)],
                        'time': [f'{hour:02d}:00' for hour in range(24)],
                        'area': self.coordinates,
                        'format': 'netcdf',
                    },
                    f'{directory}/{self.area_name}_{self.variable_name}_{year}.nc')

            self.merge_files(directory)
        else:
            # Request for each month separately
            for year in self.years_included:
                for month in range(1, 13):
                    month_str = f'{month:02d}'
                    c.retrieve(
                        'reanalysis-era5-single-levels',
                        {
                            'product_type': 'reanalysis',
                            'variable': self.variable_name,
                            'year': year,
                            'month': month_str,
                            'day': [f'{day:02d}' for day in range(1, 32)],
                            'time': [f'{hour:02d}:00' for hour in range(24)],
                            'area': self.coordinates,
                            'format': 'netcdf',
                        },
                        f'{directory}/{self.area_name}_{self.variable_name}_{year}_{month_str}.nc')

    #       Merge monthly files
    #       self.merge_files(directory)

    def merge_files(self, directory):
        """
        Merges the monthly NetCDF files into a single file and deletes the individual monthly files.

        Args:
            directory (str): Directory containing the NetCDF files.
        """
        os.chdir(directory)
        if len(self.years_included) == 1:
            merged_filename = f'{self.area_name}_{self.variable_name}_{self.years_included[0]}_complete.nc'
        else:
            merged_filename = f'{self.area_name}_{self.variable_name}_{self.years_included[0]}_{self.years_included[-1]}.nc'
        merge_command = f'cdo -b F32 mergetime *.nc {merged_filename}'
        result = subprocess.run(merge_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("Merge executed successfully")
            print("Output:", result.stdout)

            # Delete individual monthly files but keep the merged file
            delete_command = f'ls | grep -v "{merged_filename}" | xargs rm'
            result2 = subprocess.run(delete_command, shell=True, capture_output=True, text=True)

            if result2.returncode == 0:
                print("Individual files deleted successfully")
                print("Output:", result2.stdout)
            else:
                print("Deletion failed with return code", result2.returncode)
                print("Error:", result2.stderr)
        else:
            print("Merge failed with return code", result.returncode)
            print("Error:", result.stderr)

if __name__ == "__main__":
    test = Era5var('PartOfParis', [49, 1, 48, 3], '1983-2023', 'total_precipitation', monthly=True)
    test.request_data()
    # test.requestMask('FR')

    test = Era5var('PartOfParis', [49, 1, 48, 3], '1960-2023', '2m_temperature', monthly=True)
