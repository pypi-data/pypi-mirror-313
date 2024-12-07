"""
TradeUtils: for Robust API/Function Calls with correct response assurance and retries

   Copyright 2024 Sanghoon Lee (DSsoli). All Rights Reserved.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


from textwrap import dedent
import logging
import time

class TradeUtils:
    
    @staticmethod
    def retry_call(func, expected_result_type=(float, int), required_primary_key_for_dict=None, retries=5, delay=4, save_log=True, *args, **kwargs):
        """
        Retries calling a function until the expected result is obtained or the maximum number of retries is reached.
        
        Parameters:
        - func (callable): The function to be called.
        - expected_result_type (type or tuple of types): The expected type(s) of the function's return value. Defaults to (float, int).
        - required_primary_key_for_dict (str, optional): The required key if the expected result type is a dictionary. Defaults to None.
        - retries (int): The maximum number of retry attempts. Defaults to 5.
        - delay (int): The initial delay between retries in seconds. The delay doubles with each attempt. Defaults to 4.
        - save_log (bool): Whether to log errors. Defaults to True.
        - *args: Variable length argument list to be passed to the function.
        - **kwargs: Arbitrary keyword arguments to be passed to the function.

        Returns:
        - The result of the function call if it meets the expected conditions.

        Raises:
        - Exception: If the function returns None.
        - Exception: If the function returns a result of an unexpected type.
        - Exception: If the function returns a dictionary without the required primary key when expected_result_type is dict.
        - Exception: If the function fails after the maximum number of retries.

        The method performs the following steps:
        1. Attempts to call the specified function up to the maximum number of retries.
        2. Checks the result of the function call against the expected result type and required key (if applicable).
        3. Logs and prints error messages if the result is not as expected.
        4. Waits for an exponentially increasing delay between retries.
        5. Raises a final exception if all retry attempts fail.
        """
        for attempt in range(retries):
            try:
                result = func(*args, **kwargs)
                if result is None:
                    raise Exception(f"'{func.__name__}' returned '{type(result)}'")
                
                elif not isinstance(result, expected_result_type):
                    raise Exception(f"'{func.__name__}' did not return expected result type: '{expected_result_type}', but instead returned a type '{type(result)}'")
                
                elif expected_result_type == dict and isinstance(result, dict) and \
                    required_primary_key_for_dict is not None and required_primary_key_for_dict not in result:
                    raise Exception(f"'{func.__name__}' returned expected result type: '{expected_result_type}', however did not contain the required primary key: '{required_primary_key_for_dict}'")
                
                return result
            
            except Exception as e:
                message = dedent(f"""
                ==================================================
                '{func.__name__}' caused an error: 
                {e}
                Retrying... (attempt {attempt + 1} / {retries})
                ==================================================
                """)
                if save_log:
                    logging.error(message)
                print(message)
                if attempt < retries - 1:
                    time.sleep(delay * (2 ** attempt))
                else:
                    message = f"Error fetching '{func.__name__}' after {retries} retries. Error message: {e}"
                    if save_log:
                        logging.error(message)
                    print(message)
                    raise Exception(message)