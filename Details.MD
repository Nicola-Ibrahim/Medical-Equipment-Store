
**account app**:

    Models:
        Types:
            - Admin
            - Base Accountant
            - Workers Accountant
            - Warehouse Accountant
            - Statistician 
            - Warehouse
            - Doctor
            - Worker

        Base attributes:
            - Username
            - Password
            - Email
            - First name
            - Last name
            - ID


**Sales app**

    - Models:
        - Product:
            - doctor_id int
            - 

        - Order:

        - Banner:

**Admin app**

    Functionalities:
        - Check delivery workers
        - Add "Banner"
        - Send notifications: -> Doctors | Warehouse

        - Order control:
            - View pending "Orders"   
            - View pending "Orders" details   
            - Accept or reject pending "Orders"
            - Associate pending "Orders" w/ delivery worker (Search for worker)
        - Add a commission 
        - Edit a commission





**Warehouse Accountant app**

    Functionalities:
        - Accept or reject the account
        - Open a new money account
        - Send received money to DashBoard

**Workers Accountant app**

    Functionalities:
        - Accept or reject the account
        - Open a new money account
        - Send received money to DashBoard


**Warehouse app**

    Functionalities:
        - Create account
        - Product: Add, Edit, Remove
        - Indicate work days
        - Upcoming order: Accepted, Submitted, Delivered, Rejected
        - Obtain number of products sold
        - Profit percentage value
        - Indicate the visibility of a product

        

**Doctor app**

    Functionalities:
        - Create account

**Delivery worker app**

    Functionalities:
        - Create account

# TODO:  
    - Create Notification model for holding all the 
        messages that come to warehouse for delivery worker
    