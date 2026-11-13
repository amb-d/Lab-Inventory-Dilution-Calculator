from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

@dataclass
class Solution:
    name: str
    concentration: float
    volume: float
    hazardous: bool
    
@dataclass
class InventoryState:
    name: str
    current_solution: str
    solutions: list[Solution]
    calc_hist: list[str]
    
Default_State = InventoryState("", "", [], [])            

@route
def index(state: InventoryState) -> Page:
    return Page(state, [
        Header("Welcome, " + state.name),
        Paragraph("Current Active Solution: " + state.current_solution),
        Paragraph("Total Calculations Saved: " + str(len(state.calc_hist))),
        Paragraph("Choose an Action:"),
        Button("Inventory", inventory),
        Button("New Solution", add_solution_input),
        Button("Update Username", profile),
        Button("Dilution Calculator", calc_input),
        Button("About", about) ])

@route
def inventory(state: InventoryState) -> Page:
    item_display = []
    for sol in state.solutions:
        if sol.hazardous:
            item_display.append(sol.name + " - " + str(sol.volume) + "mL [SOLUTION IS DANGEROUS: PROCEED WITH CAUTION]")
        else:
            item_display.append(sol.name + " - " + str(sol.volume) + "mL")
    return Page(state, [
        Header("Current Inventory"),
        BulletedList(item_display),
        Button("Home", index) ])
                             
                             
@route
def add_solution_input(state: InventoryState) -> Page:
    return Page(state, [
        Header("Add Solution to Inventory"),
        TextBox("new_sol_name"),
        TextBox("new_sol_vol"),
        Button("Save Solution", save_new_solution),
        Button("Home", index) ])

@route
def save_new_solution(state: InventoryState, new_sol_name: str, new_sol_vol: str) -> Page:
    if new_sol_name != "":
        if new_sol_vol != "":
            vol = float(new_sol_vol)
        else:
            vol = 0.0
            
        state.solutions.append(Solution(new_sol_name, 1.0, vol, False))
        state.current_solution = new_sol_name
        
    return inventory(state)

@route
def profile(state: InventoryState) -> Page:
    return Page(state, [
        Header("Update Profile"),
        TextBox("new_name"),
        Button("Save", save_profile),
        Button("Home", index) ])

@route
def save_profile(state: InventoryState, new_name: str) -> Page:
    if new_name != "":
        state.name = new_name
        
    return index(state)

@route
def calc_input(state: InventoryState) -> Page:
    return Page(state, [
        Header("Solution Dilution Calculator"),
        Paragraph("Enter your values:"),
        TextBox("c1"),
        TextBox("c2"),
        TextBox("v2"),
        Button("Calculate", calc_result),
        Button("Home", index) ])

@route
def calc_result(state: InventoryState, c1: str, c2: str, v2: str) -> Page:
    message = "Calculation complete."
    
    if c1 == "":
        message = "Please enter an initial concentration."
        
    elif c2 == "":
        message = "Please enter a target concentration."
    
    else:
        state.calc_hist.append("Successfully ran with C1 = " + c1)
        message = "Calculation logged."
        
    return Page(state, [
        Header("Result"),
        Paragraph(message),
        Button("Calculate Another", calc_input),
        Button("Home", index) ])

@route
def about(state: InventoryState) -> Page:
    return Page(state, [
        Header("About This App"),
        Paragraph("This app can log lab inventory and track/calculate dilutions."),
        Button("Home", index) ])

test_state_1 = InventoryState("", "", [], [])
save_profile(test_state_1, "Ambrose")
assert_equal(test_state_1.name, "Ambrose")

test_state_2 = InventoryState("", "", [], [])
save_new_solution(test_state_2, "HCl", "150")
assert_equal(len(test_state_2.solutions), 1)
assert_equal(test_state_2.solutions[0].name, "HCl")
assert_equal(test_state_2.solutions[0].volume, 150.0)
assert_equal(test_state_2.current_solution, "HCl")

test_state_3 = InventoryState("Ambrose", "Water", [], [])
calc_result(test_state_3, "3.0", "1.0", "30")
assert_equal(len(test_state_3.calc_hist), 1)

set_website_title("Lab Inventory & Dilution Calculator")
set_site_information(
    author="Ambrose",
    description="A web app for tracking chemistry lab solutions and calculating dilutions.",
    sources=[],
    planning=["design.docx", "problem.docx"],
    links=["https://github.com/amb-d/Lab-Inventory-Dilution-Calculator"]
    )
hide_debug_information()
set_website_framed(False)

start_server(Default_State)

