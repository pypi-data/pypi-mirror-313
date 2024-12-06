import gspread, logging, traceback
# from gspread_formatting import format_cell_range, cellFormat, textFormat

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class fctsheet:

    def __init__(self, sheet_key=None):
        """
        sheet_name = 'profiles'
        sheet_key = 'your-sheet-key'
        fctsheet = fctsheet(sheet_key=sheet_key)
        fctsheet.delete_sheet(sheet_name=sheet_name)
        fctsheet.create_new_sheet(sheet_name=sheet_name, column_names=[])

        exclude = ['id']
        queryset = profilesModel.objects.all().values()
        filtered_data = [{key: value for key, value in record.items() if key not in exclude} for record in queryset]
        df = pd.DataFrame(filtered_data)

        fctsheet.dataframe_to_sheet(sheet_name=sheet_name, dataframe=df, overwrite=True)
        """

        self.sheet_key = sheet_key
        self.conn = None
        self.permission = False

        self.credentials_dict = {
            "type": "service_account",
            "project_id": "gmailproject-312908",
            "private_key_id": "f27243b42b4ede025c477c9f2a4f106ebcaa9fef",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCu2wtXHuMmDqeZ\n9qash+wsicdXyXHpSsssBBgFije/ii0Y1oW2Y/iNpBwS7zG3gpvmp+jYs7ufuRm8\nXRuTEMFXrj14mdz1lvCVG7LTRj8pBf76yE4UvhYfKjeYlaLtZUmoNSJOdPF4nNmx\nMogkxoMnN9eYYFgsPF4iTrl72tnkJwLVA6VBLW745fsTwahMOAbxqSVHeCe0DfTF\nZrDQHtY20HsvRUMA89WiNSAqT0z37+13TPGFkWQV8D83J4vGkgQVEkKTIJv4BxP+\n30U5yvslzQs6CcMvxWNLZjvlXCPGDezZxJC0AZictsTPX/NsMYA4PR0noso6Kxt+\nNmKBEgQrAgMBAAECggEAEZ3dCyEqsTC5ycUexB7foxnF3T4yUqxSmEkt+GTquqAG\nbMxe5WI2GQ3R4Zslbv/i4Clw8rWiWh8b4i1JSWxfO7ZrgrqRwfvmmkc+TD31asHW\nui0zJ1uCvroR/DawlxVk3I8Z4+ixVBMNdbu0bsFsq6dbJS1+b1qCVheIuttGUk+X\nJlJzH7lr9hKosDjrHtULJLeUG5a5iczRHov/gQUlHrA+eqVfoMntbq6lU86x7IpF\ng7h3cBjhFT/55faqwBlOyCA4RwK6BUs+7JdC+NV4iAWOaLhCAFjlXPVSrUZ09G26\nfZvdwoFpmQcy7OvLbtpLYMjcLTh6aFPEW7yJto350QKBgQDh/egzkgidUVWAqKRc\nWYIV4Tbg8LhKVw59ZDQfjGxX3nUuoe26NvyG1DfHzpKY9ujcWEHZRmsCX8LuyRWZ\nRW0scJrkOpEnUtihsaXN2KDWYtQCJGtWF6nlCjtex/feNgYqMOwXFvSKHheeQjSC\nXkIra/uqqP6zhkwlPEXon24DMQKBgQDGEuAr4fpETSHcNeWTWTjSRRAwYMw3AgOP\nUDLAu48nkzrFGkSmCRiswYqBHyStuhTi/ylD+MFCYswTnp9A8PiIDdv/Hw5W+l1L\nBrmGeIUhyhjKtCkvsHt55FktXGplJxa/pEaxn52742pW6fXJsvtPHwyBskPssfBE\nH30Z8DsOGwKBgQCw8IuNVRlJkxTO1ztY0vv3BY5iMBcanW7K3lmxGdD6O0KkcEQh\nOEwfhKjn1+UPvsIzQybLZ0cBZNjK/MXca28/DCs55mEf2M2kS+L1eFb1hAtaYglo\nLr7mhUxWuVposQPCpOs0aNSuD0GOt2dFa2eDd9hjlk1VYiDcRoS1zZ3lAQKBgHUa\nT8Jh9a5P08b3bmUxCLD399xCPjn/TM974KWlvbruBn7lStTG5/mq6xHvsaWsMBEM\nPf9boBZ5hqHK0+h3DtiRKRGp8LZniqSCs0jXFA6oBwRAg2EYe8fSww5YZuaqt35R\nxyHYdk7Q4tvDsnavBHkAqEo9dH8JrDz6SOH+70slAoGBAJc0WDBkjzAY0Jv0v7pz\nVFOWXT3A91H2qLiv47kuUm5JQbR0yaI1pukJRWNSBecGQcozxP02cNA/RT7SpQuN\n7jxlhTMp4Ldq8nJt/GnYodjHN5PW2MGIW3xaYkYTV1MkIqLjMpIXa761peh2BFJ8\ns7Qk/1mSMB1tLsn5SLKtZc/2\n-----END PRIVATE KEY-----\n",
            "client_email": "khemiri@gmailproject-312908.iam.gserviceaccount.com",
            "client_id": "105233633854083449874",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/khemiri%40gmailproject-312908.iam.gserviceaccount.com"
        }
        try:
            gc = gspread.service_account_from_dict(self.credentials_dict)
            self.conn = gc.open_by_key(self.sheet_key)
            self.permission = True
        except:
            if 'The caller does not have permission' in traceback.format_exc():
                logging.warning(f'The caller does not have permission to access the spreadsheet "{sheet_key}"')
            else:
                logging.error(traceback.format_exc())


    def get_all_sheet_names(self):
        """
        Retrieve all sheet names in the Google Sheets file.

        Example:
        fctsheet = fctsheet(sheet_key="your-sheet-key")
        sheet_names = fctsheet.get_all_sheet_names()
        """
        try:
            if self.permission:
                return [sheet.title for sheet in self.conn.worksheets()]
            else:
                return []
        except Exception as e:
            logging.error(f"Failed to retrieve sheet names. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return []

    def create_new_sheet(self, sheet_name, column_names):
        """
        Create a new sheet with the specified name and column names,
        with options to delete the sheet before creating it.

        Args:
        - sheet_name (str): Name of the sheet.
        - column_names (list): List of column names to add in the first row.

        Example:
        fctsheet.create_new_sheet(sheet_name="NewSheet", column_names=['user', 'pass'])
        """
        try:
            # Check if the sheet exists
            if self.sheet_exists(sheet_name):
                logging.info(f"Sheet '{sheet_name}' already exists. No new sheet created.")
                return

            # Determine the number of columns based on the column_names list length
            new_sheet = self.conn.add_worksheet(title=sheet_name, rows=1, cols=len(column_names))

            # Populate the first row with column names
            new_sheet.insert_row(column_names, 1)

            logging.info(f"Sheet '{sheet_name}' created successfully")
        except Exception as e:
            logging.error(f"Failed to create sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())


    def truncate_sheet(self, sheet_name):
        """
        Truncate (clear) all data in the specified sheet if it exists.

        Args:
        - sheet_name (str): Name of the sheet.

        Example:
        fctsheet.truncate_sheet(sheet_name="ExistingSheet")
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)
                sheet.clear()
                sheet.resize(rows=1)
                logging.info(f"Sheet '{sheet_name}' truncated successfully.")
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist. No truncation performed.")
        except Exception as e:
            logging.error(f"Failed to truncate sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())



    def delete_sheet(self, sheet_name):
        """
        Delete the sheet with the specified name if it exists.

        Args:
        - sheet_name (str): Name of the sheet.

        Example:
        fctsheet.delete_sheet(sheet_name="ExistingSheet")
        """
        try:
            if self.sheet_exists(sheet_name):
                # Retrieve the sheet object
                sheet = self.conn.worksheet(sheet_name)
                self.conn.del_worksheet(sheet)  # Delete the sheet
                logging.info(f"Sheet '{sheet_name}' deleted successfully.")
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist. No deletion performed.")
        except Exception as e:
            logging.error(f"Failed to delete sheet '{sheet_name}'. Error: {str(e)}")


    def sheet_exists(self, sheet_name):
        """
        Check if a sheet with the specified name exists.

        Args:
        - sheet_name (str): Name of the sheet.

        Example:
        sheet_exists = fctsheet.sheet_exists(sheet_name="ExistingSheet")
        print(f"Sheet exists: {sheet_exists}")
        """
        try:
            if self.permission:
                sheet_names = self.get_all_sheet_names()
                return sheet_name in sheet_names
            else:
                return False
        except Exception as e:
            logging.error(f"Failed to check if sheet exists. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return False


    def count_rows(self, sheet_name, count_header=False):
        """
        Count all rows in the specified sheet, optionally excluding the header row.

        Args:
        - sheet_name (str): Name of the sheet.
        - count_header (bool): Whether to count the header row. Default is False, meaning the header row is excluded from the count.

        Example:
        row_count = fctsheet.count_rows(sheet_name="ExistingSheet", count_header=False)
        logging.info(f"Row count: {row_count}")
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)
                all_rows = sheet.get_all_values()

                # If count_header is True, exclude the first row (header)
                row_count = len(all_rows) if count_header else len(all_rows) - 1
                return max(row_count, 0)  # Ensure non-negative count
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return 0
        except Exception as e:
            logging.error(f"Failed to count rows in sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return 0

    def get_all_values(self, sheet_name):
        """
        Get all values from the specified sheet and return them as a list of dictionaries
        where each key is the column name and each value is the corresponding row's value.

        Args:
        - sheet_name (str): Name of the sheet.

        Example:
        values = fctsheet.get_all_values(sheet_name="ExistingSheet")
        logging.info(f"values: {values}")
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)
                all_values = sheet.get_all_values()

                if not all_values:
                    logging.info(f"No data found in sheet '{sheet_name}'.")
                    return []

                # The first row contains column names
                headers = all_values[0]

                # Create a list of dictionaries with column names as keys
                data = [
                    dict(zip(headers, row)) for row in all_values[1:]
                ]

                return data
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return []
        except Exception as e:
            logging.error(f"Failed to retrieve values from sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return []


    def get_value_at(self, sheet_name, cell_ref):
        """
        Get the value from a specific cell (e.g., 'A2') in the sheet.

        Args:
        - sheet_name (str): Name of the sheet.
        - cell_ref (str): The cell reference (e.g., 'A2') from which to get the value.

        Example:
        value = fctsheet.get_value_at(sheet_name="ExistingSheet", cell_ref="A2")
        logging.info(f"value: {value}")
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)
                value = sheet.acell(cell_ref).value
                return value
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return None
        except Exception as e:
            logging.error(f"Failed to retrieve value from sheet '{sheet_name}' at cell {cell_ref}. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return None

    def insert(self, sheet_name, values):
        """
        Insert a new row at the end of the sheet with the provided values (as a dictionary)
        and return the ID of the inserted row.

        Args:
        - sheet_name (str): Name of the sheet.
        - values (dict): Dictionary of values to insert, where keys are column names.

        Returns:
        - last_id (int): The ID (row number) of the newly inserted row.

        Example:
        values = {"cookies": "new cookies", "active": "pmsk"}
        last_id = fctsheet.insert(sheet_name="ExistingSheet", values=values)
        logging.info(f"Inserted row ID: {last_id}")
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)

                # Get the headers (column names) from the first row
                headers = sheet.row_values(1)

                # Map the dictionary values to the correct columns based on header names
                row_values = [values.get(header, "") for header in headers]

                # Append the new row with mapped values
                sheet.append_row(row_values)

                # Get the current number of rows (last inserted row's ID)
                last_id = len(sheet.get_all_values())

                logging.info(f"Inserted new row in '{sheet_name}' at row ID: {last_id}")
                return last_id
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return None
        except Exception as e:
            logging.error(f"Failed to insert row in sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return None


    def update(self, sheet_name, filter, values):
        """
        Update all rows in the specified sheet that match the filter criteria,
        where filter criteria is a dictionary with column names as keys and
        values as the values to filter on.

        Args:
        - sheet_name (str): Name of the sheet.
        - filter (dict): A dictionary where keys are column names and
          values are the values to filter on.
        - values (dict): A dictionary of column names and their new values
          to update the matching rows.

        Example:
        fctsheet.update(
            sheet_name="ExistingSheet",
            filter={"Name": "Alice", "Age": "25"},
            values={"City": "Boston", "Age": "26"}
        )
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)
                all_values = sheet.get_all_values()

                if not all_values:
                    logging.info(f"No data found in sheet '{sheet_name}'.")
                    return False

                # The first row contains column headers
                headers = all_values[0]

                # Find the index of the columns to update based on headers
                filter_columns = [headers.index(col) for col in filter.keys()]
                update_columns = {headers.index(col): value for col, value in values.items()}

                rows_updated = 0

                # Iterate over all rows and update the ones that match the filter criteria
                for row_idx, row in enumerate(all_values[1:], start=1):  # Skip the header row
                    # Check if the row matches the filter criteria
                    if all(row[filter_columns[i]] == list(filter.values())[i] for i in
                           range(len(filter))):
                        # Update the row with new values
                        for col_idx, new_value in update_columns.items():
                            row[col_idx] = str(new_value)

                        # Update the sheet with the modified row
                        sheet.update('A' + str(row_idx + 1), [row])

                        # # Apply plain text format to all columns in the updated row
                        # range_to_format = f"A{row_idx + 1}:{chr(65 + len(row) - 1)}{row_idx + 1}"  # Range for the updated row
                        # format_cell_range(sheet, range_to_format, cellFormat(textFormat=textFormat()))

                        rows_updated += 1

                if rows_updated > 0:
                    logging.info(f"Updated {rows_updated} rows in sheet '{sheet_name}'.")
                    return True
                else:
                    logging.info(f"No rows found matching filter criteria in sheet '{sheet_name}'.")
                    return False
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return False
        except Exception as e:
            logging.error(f"Failed to update rows in sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return False


    def dataframe_to_sheet(self, sheet_name, dataframe, overwrite=False):
        """
        Insert a DataFrame into a Google Sheet. Optionally overwrite the existing sheet.

        Args:
        - sheet_name (str): Name of the sheet.
        - dataframe (pd.DataFrame): The Pandas DataFrame to insert into the sheet.
        - overwrite (bool): Whether to overwrite the existing sheet with new data. Default is False.

        Example:
        import pandas as pd
        df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
        fctsheet.dataframe_to_sheet(sheet_name="MySheet", dataframe=df, overwrite=True)
        """
        try:
            if self.sheet_exists(sheet_name):
                sheet = self.conn.worksheet(sheet_name)

                # If overwrite is True, truncate the existing sheet
                if overwrite:
                    self.truncate_sheet(sheet_name)

                # Convert the DataFrame to a list of lists (rows)
                rows = [dataframe.columns.values.tolist()] + dataframe.values.tolist()

                # Update the sheet with the new data
                sheet.update('A1', rows)  # Start updating from the first cell

                logging.info(f"Data from DataFrame inserted into '{sheet_name}' sheet.")
            else:
                logging.info(f"Sheet '{sheet_name}' does not exist.")
                return None
        except Exception as e:
            logging.error(f"Failed to insert DataFrame into sheet '{sheet_name}'. Error: {str(e)}")
            logging.error(traceback.format_exc())
            return None


# if __name__ == '__main__':
    #fctsheet = fctsheet(sheet_key='SHEET_KEY')

    # sheet_names = fctsheet.get_all_sheet_names()
    # logging.info(f'sheet_names: {sheet_names}')

    # column_names = [f'user_{i+1}' for i in range(200)]
    # fctsheet.create_new_sheet(sheet_name="NewSheet", column_names=column_names)

    # values = fctsheet.get_all_values(sheet_name="NewSheet")
    # logging.info(f"values: {values}")

    # value = fctsheet.get_value_at(sheet_name="NewSheet", cell_ref='G8')
    # logging.info(f"value: {value}")

    # values = {"cookies": "new cookies", "active": "pmsk"}
    # value = fctsheet.insert(sheet_name="NewSheet", values=values)
    # logging.info(f"value: {value}")

    # fctsheet.update(
    #     sheet_name="NewSheet",
    #     filter={"username": "Priya&1234"},
    #     values={"cookies": "new cookies", "active": "pmsk"}
    # )

    # import pandas as pd
    # df = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
    # fctsheet.dataframe_to_sheet(sheet_name="NewSheet", dataframe=df, overwrite=True)