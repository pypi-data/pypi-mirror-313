import py4j
import re
from datetime import datetime


class DbxWidget:
    """
    A utility class for interacting with Databricks widgets to read and create widget values.

    Usage:
    - To read the value from an existing widget:
        value = DbxWidget(dbutils, widget_name)

    - To create a new widget with specified type and options:
        value = DbxWidget(dbutils, widget_name, type='dropdown', defaultValue='Red', choices=["Red", "Blue", "Yellow"])

    Inputs:
    - dbutils: Databricks utility object for widget operations
    - name: Name of the widget
    - type: Type of the widget (text, dropdown, multiselect, combobox). Defaults to Text if not provided
    - defaultValue: Default value for the widget. Defaults to blank
    - **kwargs: Additional keyword arguments for widget creation

    Example:
    - Existing method:
        dbutils.widgets.dropdown("colour", "Red", "Enter Colour", ["Red", "Blue", "Yellow"])
        colour = dbutils.widgets.read("colour")

    - New method:
        colour = DbxWidget(dbutils, "colour", 'dropdown', "Red", choices=["Red", "Blue", "Yellow"])
    """

    def __new__(self, dbutils, name, type='text', defaultValue='', returntype='text', **kwargs):
        if name is None:
            raise ValueError("Widget name cannot be blank")
        
        if not re.match(r'^\w+$', name):
            raise ValueError("Widget name must contain only alphanumeric characters or underscores")
        
        if type not in ['text', 'dropdown', 'multiselect', 'combobox']:
            raise ValueError("Invalid widget type. Supported types: text, dropdown, multiselect, combobox")
        
        if type in ['dropdown', 'multiselect'] and 'choices' not in kwargs:
            raise ValueError("Choices list is required for dropdown widgets")          
         
        valid_return_types = ['text', 'int', 'double', 'float','date']
        if returntype not in valid_return_types:
            raise ValueError(f"Invalid return type. Supported types: {', '.join(valid_return_types)}")

        widgetName = re.sub(r'\W|^(?=\d)', '_', name)
        
        widgetConstructor = {
            'text': dbutils.widgets.text,
            'dropdown': dbutils.widgets.dropdown,
            'multiselect': dbutils.widgets.multiselect,
            'combobox': dbutils.widgets.combobox
        }[type]
        
        try:
            returnValue = dbutils.widgets.get(widgetName)
        except py4j.protocol.Py4JJavaError as e:
            if 'No input widget' in str(e.java_exception):
                try:
                    widgetConstructor(name=widgetName, defaultValue=defaultValue, label=name, **kwargs)
                    returnValue = dbutils.widgets.get(widgetName)
                except Exception as e:
                    raise ValueError(f"Error creating widget: {e}")
            else:
                raise e
            
        if returntype == 'int':
            try:
                returnValue = int(returnValue)
            except ValueError:
                raise ValueError("Widget value cannot be converted to an integer")
        elif returntype in ['double','float']:
            try:
                returnValue = float(returnValue)
            except ValueError:
                raise ValueError("Widget value cannot be converted to a double")
        elif returntype == 'date':
            try:
                date_format = "%Y-%m-%d"
                parsed_date = datetime.strptime(returnValue, date_format).date()
                returnValue = parsed_date
            except ValueError:
                raise ValueError("Widget value is not in the format yyyy-mm-dd")

        return returnValue
  