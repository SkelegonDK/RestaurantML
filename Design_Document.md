# Restaurant Inventory Management System: Design Document

## 1. Overall Layout

The application will follow a consistent layout across all pages:

- Left Sidebar (Grey): Dashboard and navigation
- Top Bar (Yellow): Fixed input area for natural language queries
- Main Content Area (Blue): Displays responses, content, and analytics
- Background (Black): Provides contrast

## 2. Component Details

### 2.1 Left Sidebar (Dashboard)
- Restaurant name/logo
- Navigation menu
- Key metrics (e.g., low stock alerts, upcoming expiration dates)
- User authentication status

### 2.2 Top Bar (Query Input)
- Text input field for natural language queries
- Send button
- Optional: Quick action buttons for common queries

### 2.3 Main Content Area
- Dynamically changes based on the selected page
- Pages include: Home, Inventory, Recipes, Query Results, Analytics

### 2.4 Footer
- Version information
- Links to help/documentation

## 3. Page Designs

### 3.1 Home Page
- Welcome message
- Summary of current inventory status
- Quick links to key actions (e.g., "Add New Recipe", "Update Inventory")

### 3.2 Inventory Page
- Searchable and sortable table of ingredients
- Columns: Name, Quantity, Unit, Expiration Date, Actions
- Color-coding based on stock levels and expiration dates
- "Add New Ingredient" button
- Filters for categories, expiration ranges, etc.

### 3.3 Recipes Page
- List view of all recipes
- Each recipe card shows: Name, main ingredients, serving size
- Search and filter options
- "Add New Recipe" button
- Clicking a recipe opens a detailed view

### 3.4 Query Results Page
- Displays responses to natural language queries
- List of suggested dishes based on inventory
- Option to view full recipe details
- Substitution suggestions if ingredients are low/missing

### 3.5 Analytics Page
- Various charts and graphs using Plotly
- Inventory usage over time
- Most popular dishes
- Waste reduction metrics
- Cost efficiency analysis

## 4. Color Scheme
- Background: #000000 (Black)
- Sidebar: #D3D3D3 (Light Gray)
- Input Bar: #FFFF00 (Yellow)
- Main Content: #4682B4 (Steel Blue)
- Accent: #FF4500 (Orange-Red) for alerts and important actions

## 5. Typography
- Headers: Sans-serif (e.g., Roboto)
- Body: Serif (e.g., Lora)
- Monospace for code or query examples

## 6. Responsive Design
- Optimize layout for desktop, tablet, and mobile views
- Collapsible sidebar for smaller screens
- Adjustable chart sizes in analytics

## 7. Accessibility Considerations
- High contrast color options
- Keyboard navigation support
- Screen reader compatible elements
- Clear, descriptive alt text for images and icons

## 8. Future Enhancements
- Dark/Light mode toggle
- Customizable dashboard widgets
- Integration with POS systems for real-time inventory updates
- Mobile app for inventory management on-the-go