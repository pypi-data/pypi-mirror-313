Overview
=============


This library streamlines the process of creating data classes and offers a versatile configuration model. It also enables the dumping and restoration of data. This library is built on Pydantic.

Installation
=============


You can add it to your project using the following command:

`pip install t-object`

After installing, you can import it into your project using the command

`from t_object import ThoughtfulObject`.

Make sure to check the documentation for detailed usage instructions and examples.


Key features you need to know
=============================


1. All features of the original Pydantic library are available.
---------------------------------------------------------------

- Creating models

.. code-block:: python

    class Driver(ThoughtfulObject):
        name: str
        age: int
        driving_experience: timedelta
        last_driving_date: datetime

    class Car(ThoughtfulObject):
        model: str
        car_release_date: date
        price: float
        driver: list[Driver]


and

.. code-block:: python

    class Patient(ThoughtfulObject):
        name: str
        age: int
        birth_date: datetime

- creating instanse of model

.. code-block:: python

    car = Car(
        model="Tesla Model S",
        car_release_date=date(2012, 6, 22),
        price=79999.99,
        driver=[
                Driver(
                    name="Elon Musk",
                    age=49,
                    driving_experience=timedelta(days=365 * 30),
                    last_driving_date=datetime(2021, 1, 1)
        ),
            Driver(
                  name="Jeff Bezos",
                  age=57,
                  driving_experience=timedelta(days=365 * 20),
                  last_driving_date=datetime(2021, 1, 1)
         )]
    )

and

.. code-block:: python

    patient = Patient(
        name="John Doe",
        age=42,
        birth_date=datetime(1979, 1, 1)
    )

2. Configuration
-----------------

- Default configuration of the T-Object. Simply import it using `from t_object import ThoughtfulObject`. Default configuration listed below.

.. code-block:: python

    validate_assignment=True,
    extra=Extra.forbid,
    frozen=False,
    populate_by_name=False,
    arbitrary_types_allowed=True,
    allow_inf_nan=True,
    strict=True,
    revalidate_instances=RevalidateInstances.always,
    validate_default=False,
    coerce_numbers_to_str=True,
    validation_error_cause=True,
    str_strip_whitespace=True,


- For custom configuration, use the `build_custom_t_object` function. You can find all configuration flags at https://docs.pydantic.dev/2.6/api/config/. Here is how to use it

.. code-block:: python

    ResponseObject = build_custom_t_object(
          extra=Extra.allow,
          frozen=True,
          allow_inf_nan=True,
          strict=False,
    )
    class UserResponse(ResponseObject):
        name: str
        age: int
        dob: datetime

3. Exporting the model to JSON format
--------------------------------------


- To export data, use the `save_to_json_file()` method. You can either define the file path manually or leave it blank for automatic naming.


4. Importing JSON into the Model
---------------------------------


- To import data from a JSON file, use the `load_from_json_file(file_path: str)` class method. This method validates the data against your model automatically. The `file_path` attribute is required, which is the path to the JSON file.

.. code-block:: python

    patient = Patient.load_from_json_file("patient.json")

5. Pretty String
-----------------


It is possible to print any instance in a more readable and attractive format. This formatting can be achieved by employing the pretty_string() method. This method allows for the effortless transformation of the raw data into a format that is easier on the eyes,