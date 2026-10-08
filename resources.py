# ==========================================
# INITIAL DATA STRUCTURES
# ==========================================
resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}

]

fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}

# Every log is a dict: {"fellow_id": str, "resource_id": str, "quantity": int}
borrow_records = []

# ==========================================
# CORE INVENTORY & TRANSACTION MANAGEMENT
# ==========================================
def add_resource(res_id, name, category, total_units):
    """Requirement 1: Adds a new resource while rejecting duplicate IDs."""
    for res in resources:
        if res["id"].upper() == res_id.upper():
            print(f"Error: Resource ID '{res_id}' already exists!")
            return False
    
    new_res = {
        "id": res_id,
        "name": name,
        "category": category,
        "total": total_units,
        "available": total_units
    }
    resources.append(new_res)
    print(f"Success: Resource '{name}' added successfully.")
    return True

def list_resources():
    """Requirement 1: Lists all current resources."""
    print("\n--- Current Inventory ---")
    for res in resources:
        print(f"ID: {res['id']} | Name: {res['name']} | Category: {res['category']} | Total: {res['total']} | Available: {res['available']}")

def borrow_resource(fellow_id, resource_id, quantity):
    """Requirement 2: Validates and logs resource borrowing."""
    if fellow_id not in fellows:
        print(f"Error: Fellow ID '{fellow_id}' does not exist.")
        return False
        
    if quantity <= 0:
        print("Error: Borrow quantity must be a positive integer.")
        return False
        
    target_res = None
    for res in resources:
        if res["id"].upper() == resource_id.upper():
            target_res = res
            break
            
    if not target_res:
        print(f"Error: Resource ID '{resource_id}' does not exist.")
        return False
        
    if quantity > target_res["available"]:
        print(f"Error: Cannot borrow {quantity} unit(s). Only {target_res['available']} available.")
        return False
        
    # State mutation happens safely here
    target_res["available"] -= quantity
    borrow_records.append({
        "fellow_id": fellow_id,
        "resource_id": target_res["id"],
        "quantity": quantity
    })
    print(f"Success: {fellows[fellow_id]} borrowed {quantity}x {target_res['name']}(s). Available remaining: {target_res['available']}")
    return True

def get_fellow_active_loans(fellow_id, resource_id):
    """Helper to calculate net borrowed units of a specific resource by a fellow."""
    net_borrowed = 0
    for record in borrow_records:
        if record["fellow_id"] == fellow_id and record["resource_id"].upper() == resource_id.upper():
            net_borrowed += record["quantity"]
    return net_borrowed

def return_resource(fellow_id, resource_id, quantity):
    """Requirement 3: Accepts returns only if quantity matches active loans."""
    if fellow_id not in fellows:
        print(f"Error: Fellow ID '{fellow_id}' does not exist.")
        return False
        
    if quantity <= 0:
        print("Error: Return quantity must be a positive integer.")
        return False

    target_res = None
    for res in resources:
        if res["id"].upper() == resource_id.upper():
            target_res = res
            break
            
    if not target_res:
        print(f"Error: Resource ID '{resource_id}' does not exist.")
        return False

    net_borrowed = get_fellow_active_loans(fellow_id, resource_id)
    if quantity > net_borrowed:
        print(f"Error: Return rejected. {fellows[fellow_id]} has only {net_borrowed} unit(s) of {target_res['name']} on loan.")
        return False

    # Update states
    target_res["available"] += quantity
    
    # Neutralize the borrow history tracking
    borrow_records.append({
        "fellow_id": fellow_id,
        "resource_id": target_res["id"],
        "quantity": -quantity
    })
    print(f"Success: {fellows[fellow_id]} returned {quantity}x {target_res['name']}(s). Available now: {target_res['available']}")
    return True

# ==========================================
# SEARCH & REPORTING
# ==========================================
def search_inventory(query_name=None, category=None):
    """Requirement 4: Case-insensitive search and/or category filtering."""
    results = resources
    
    if query_name:
        results = [r for r in results if query_name.lower() in r["name"].lower()]
    if category:
        results = [r for r in results if r["category"].lower() == category.lower()]
        
    print(f"\n--- Search Results (Name: '{query_name}', Category: '{category}') ---")
    if not results:
        print("No matching resources found.")
    for res in results:
        print(f"ID: {res['id']} | Name: {res['name']} | Category: {res['category']} | Available: {res['available']}/{res['total']}")

def generate_report():
    """Requirement 5: Aggregates metrics, lists shortages, and checks loan leaders."""
    total_units = sum(r["total"] for r in resources)
    available_units = sum(r["available"] for r in resources)
    borrowed_units = total_units - available_units
    
    low_stock = [r for r in resources if r["available"] < 3]
    
    # Calculate current borrow counts per item type
    borrow_counts = {}
    for res in resources:
        borrow_counts[res["id"]] = res["total"] - res["available"]
        
    max_borrowed = max(borrow_counts.values()) if borrow_counts else 0
    
    most_borrowed_resources = []
    if max_borrowed > 0:
        most_borrowed_resources = [r["name"] for r in resources if borrow_counts[r["id"]] == max_borrowed]

    print("\n================ SYSTEM REPORT ================")
    print(f"Total Stock Units:            {total_units}")
    print(f"Total Available Units:        {available_units}")
    print(f"Total Borrowed Units:         {borrowed_units}")
    print("-----------------------------------------------")
    print("Low Stock Resources (< 3 units available):")
    if not low_stock:
        print("  None")
    for r in low_stock:
        print(f"  - {r['name']} ({r['available']} available)")
    print("-----------------------------------------------")
    print(f"Most Borrowed Resource(s) (Count: {max_borrowed}):")
    if not most_borrowed_resources:
        print("  None")
    for name in most_borrowed_resources:
        print(f"  - {name}")
    print("===============================================")

# ==========================================
# INTERACTIVE CONSOLE MENU
# ==========================================
def run_menu():
    """Requirement 6: Loop driven application interface with input checking."""
    while True:
        print("\n=== LEARN2EARN EQUIPMENT MANAGEMENT ===")
        print("1. Add Resource")
        print("2. List All Resources")
        print("3. Borrow Equipment")
        print("4. Return Equipment")
        print("5. Search Inventory")
        print("6. Generate Report")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == "1":
            res_id = input("Enter Resource ID (e.g., R004): ").strip()
            name = input("Enter Resource Name: ").strip()
            category = input("Enter Category: ").strip()
            try:
                total = int(input("Enter Total Stock Quantity: "))
                if total <= 0:
                    print("Quantity must be greater than zero.")
                    continue
                add_resource(res_id, name, category, total)
            except ValueError:
                print("Error: Total units must be a valid integer.")
                
        elif choice == "2":
            list_resources()
            
        elif choice == "3":
            fellow_id = input("Enter Fellow ID (e.g., F001): ").strip().upper()
            res_id = input("Enter Resource ID (e.g., R001): ").strip().upper()
            try:
                qty = int(input("Enter Quantity to Borrow: "))
                borrow_resource(fellow_id, res_id, qty)
            except ValueError:
                print("Error: Borrow quantity must be an integer.")
                
        elif choice == "4":
            fellow_id = input("Enter Fellow ID (e.g., F001): ").strip().upper()
            res_id = input("Enter Resource ID (e.g., R001): ").strip().upper()
            try:
                qty = int(input("Enter Quantity to Return: "))
                return_resource(fellow_id, res_id, qty)
            except ValueError:
                print("Error: Return quantity must be an integer.")
                
        elif choice == "5":
            name_q = input("Search by name (Press Enter to skip): ").strip()
            cat_q = input("Filter by category (Press Enter to skip): ").strip()
            search_inventory(query_name=name_q if name_q else None, category=cat_q if cat_q else None)
            
        elif choice == "6":
            generate_report()
            
        elif choice == "7":
            print("System Exited. Thank you!")
            break
        else:
            print("Invalid Option! Please select an explicit choice from 1 to 7.")

if __name__ == "__main__":
    run_menu()
