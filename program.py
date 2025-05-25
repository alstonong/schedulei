import dearpygui.dearpygui as dpg
import function

def main():
    dpg.create_context()

    # -----
    function.loadalldata()
    function.menuwindow()
    function.addnewvegetablewindow()
    function.addduplicatevegetablewindow()
    function.ingredientswindow()
    function.vegetableswindow()
    function.checklistwindow()
    # -----

    dpg.create_viewport(title='Schedule I', width=1400, height=700)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__': main()

'''
Base data

{
    "ingredients": [
        {"ingredientid": 0, "name": "cuke", "cost": 2},
        {"ingredientid": 1, "name": "banana", "cost": 2},
        {"ingredientid": 2, "name": "paracetamol", "cost": 3},
        {"ingredientid": 3, "name": "donut", "cost": 3},
        {"ingredientid": 4, "name": "viagor", "cost": 4},
        {"ingredientid": 5, "name": "mouth wash", "cost": 4},
        {"ingredientid": 6, "name": "flu medicine", "cost": 5},
        {"ingredientid": 7, "name": "gasoline", "cost": 5},
        {"ingredientid": 8, "name": "energy drink", "cost": 6},
        {"ingredientid": 9, "name": "motor oil", "cost": 6},
        {"ingredientid": 10, "name": "mega bean", "cost": 7},
        {"ingredientid": 11, "name": "chilli", "cost": 7},
        {"ingredientid": 12, "name": "battery", "cost": 8},
        {"ingredientid": 13, "name": "iodine", "cost": 8},
        {"ingredientid": 14, "name": "addy", "cost": 9},
        {"ingredientid": 15, "name": "horse semen", "cost": 9}
    ],
    "vegetables": [
        {"vegetableid": 0, "name": "og kush", "dependencies": [-1, -1], "sale": 38, "costty": 3.75, "costtpy": 5.0, "costpy": 2.5, "costppy": 3.75, "profitty": 34.25, "profittpy": 33.0, "profitpy": 35.5, "profitppy": 34.25},
        {"vegetableid": 1, "name": "sour diesel", "dependencies": [-1, -1], "sale": 40, "costty": 4.375, "costtpy": 5.416666666666667, "costpy": 2.9166666666666665, "costppy": 4.0625, "profitty": 35.625, "profittpy": 34.583333333333336, "profitpy": 37.083333333333336, "profitppy": 35.9375},
        {"vegetableid": 2, "name": "green crack", "dependencies": [-1, -1], "sale": 43, "costty": 5.0, "costtpy": 5.833333333333333, "costpy": 3.3333333333333335, "costppy": 4.375, "profitty": 38.0, "profittpy": 37.166666666666664, "profitpy": 39.666666666666664, "profitppy": 38.625},
        {"vegetableid": 3, "name": "granddaddy purple", "dependencies": [-1, -1], "sale": 44, "costty": 5.625, "costtpy": 6.25, "costpy": 3.75, "costppy": 4.6875, "profitty": 38.375, "profittpy": 37.75, "profitpy": 40.25, "profitppy": 39.3125}
    ]
}
'''