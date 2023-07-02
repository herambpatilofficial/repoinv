# Inventory Management for Franchisee Stores

This project is an inventory management system for franchisee stores built using Django and Tailwind CSS.

## Features

- **User Authentication**: The application leverages Django's built-in authentication system to provide secure user registration and login functionality.
- **Dashboard**: Upon logging in, users are presented with a dashboard that provides an overview of key inventory metrics, sales data, and notifications.
- **Inventory Management**: Users can add, update, and delete products in the inventory. Each product entry includes details such as name, description, price, and quantity.
- **Stock Management**: The system allows users to track stock levels of each product and receive notifications for low stock items, enabling timely restocking.
- **Purchase Orders**: Users can generate purchase orders based on low stock items or predicted demand. The application provides features for managing and tracking purchase orders.
- **Sales Tracking**: The system tracks sales made by the franchisee store, providing insights into product performance and sales trends.
- **Reporting**: Customized reports can be generated to analyze inventory levels, sales performance, and other relevant metrics, aiding in decision-making processes.
- **Notifications**: Users receive notifications for important inventory updates, low stock items, and pending purchase orders to stay informed about the system's status.

## Workflow

1. **User Registration and Login**: Users can create an account and log in using their credentials.
2. **Dashboard Overview**: Upon logging in, users are presented with an interactive dashboard displaying key inventory metrics, sales data, and notifications.
3. **Inventory Management**: Users can add new products, update existing product details, and delete products from the inventory using intuitive forms.
4. **Stock Monitoring**: The system provides a clear overview of stock levels for each product, highlighting low stock items for attention.
5. **Purchase Order Generation**: Users can generate purchase orders based on low stock items or predicted demand, specifying the required quantity and supplier information.
6. **Purchase Order Management**: Users can track and manage purchase orders, including updating delivery information and marking orders as completed upon receipt of stock.
7. **Sales Tracking**: The system records sales made by the franchisee store, allowing users to view sales history, including details such as the product sold, quantity, and date of sale.
8. **Reporting and Analysis**: Customized reports can be generated to analyze inventory levels, sales performance, and other relevant metrics, assisting in data-driven decision-making.
9. **Notifications**: Users receive notifications for important inventory updates, low stock items, and pending purchase orders, ensuring timely actions to maintain sufficient stock levels.

## Installation and Usage

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the database and run migrations using `python manage.py migrate`.
4. Start the development server with `python manage.py runserver`.
5. Access the application through your browser at `http://localhost:8000`.

Please note that this is a basic setup guide. You may need to adjust the instructions according to your specific environment and deployment requirements.

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

Refer to issues and kindly contribute:
1. Better and optimized frontend
2. Visually appealing dashboard
3. Currently purchase model is only for superuser, once she generates a purchase, inventory of respective stores get updated, Add an option to let vendors request inventory
4. Any more features
5. Contribution for better documentation

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize and modify the project according to your needs.
