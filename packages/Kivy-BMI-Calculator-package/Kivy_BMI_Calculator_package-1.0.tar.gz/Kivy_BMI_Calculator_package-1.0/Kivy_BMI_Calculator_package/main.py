from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


# This is a class for displaying the result of the BMI calculation
class Result_popup(Popup):
    def answers(self, bmi, advanced, ideal_weight):
        if bmi < 16:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Severely underweight"
        elif bmi < 16.9:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Underweight"
        elif bmi < 18.5:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Mild Underweight"
        elif bmi < 24.9:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Ideal"
        elif bmi < 29.9:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Overweight"
        elif bmi < 34.9:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Obese Class 1"
        elif bmi < 39.9:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Obese Class 2"
        elif bmi > 40:
            self.ids.bmi_number.text = "BMI number "+str(bmi)
            self.ids.result.text = "Your status is: Obese Class 3"

        if advanced == "True":
            adv = Label(text="The ideal weight for your height should be between %s kg and %s kg" % (round(ideal_weight[0],2), round(ideal_weight[1],2)))
            self.ids.advanced_results.add_widget(adv)
            self.ids.advanced_results.size_hint = (1, 0.3)
        else:
            self.ids.advanced_results.clear_widgets()
            self.ids.advanced_results.size_hint = (1, 0.1)
        self.open()

# This is a class for displaying the error messages if they happen sometime during the calculation
class Error_popup(Popup):
    def reason(self, reason):
        self.ids.reason.text = reason
        self.open()

# This is a class for the advanced form that will be displayed if the user chooses to use it
class Advanced_form(GridLayout):
    pass

# This is the main grid of the app
class Main_grid(GridLayout):

    # this is a method that gets the ideal weight a certain height and gender, it is enabled only if the user chooses to use the advanced form
    def get_ideal_weight(self):
        height = float(self.ids.height.text)
        gender = self.grid.ids.gender.text
        if self.system == "Metric":
            height = height/2.54 # this is to convert cm to inches
        extra_inches = height - 60
        adjustment = extra_inches * 2.3
        if gender == "Male":
            ideal_weight = 50 + adjustment
        else:
            ideal_weight = 45.5 + adjustment
        obj = [ideal_weight-ideal_weight*0.1, ideal_weight+ideal_weight*0.1]
        return obj

    # method to get the BMI value
    def get_bmi(self):
        height = float(self.ids.height.text)
        weight = float(self.ids.weight.text)
        if self.system == "Metric":
            height = height/100 # this is to convert cm to m
            bmi = weight / (height ** 2)
        else:
            bmi = 703 * (weight / (height ** 2))
        return round(bmi, 2)
    
    # this is a method to check if the values entered by the user are valid
    def check_bmi(self):
        if self.system == "Metric":
            if self.ids.height.text == "" or self.ids.weight.text == "" or int(self.ids.height.text) < 120 or int(self.ids.height.text) > 300 or int(self.ids.weight.text) < 30 or int(self.ids.weight.text) > 300:
                err_pop = Error_popup()
                err_pop.reason("Please enter valid values for height and weight")
                return False
            else:
                if self.advanced == "True":
                    if self.grid.ids.gender.text == "select":
                        err_pop = Error_popup()
                        err_pop.reason("Please enter valid values for age and gender")
                        return False
                    else:
                        return True
                else:
                    return True
        else:
            if self.ids.height.text == "" or self.ids.weight.text == "" or int(self.ids.height.text) > 96 or int(self.ids.height.text) < 60 or int(self.ids.weight.text) > 700 or int(self.ids.weight.text) < 40:
                err_pop = Error_popup()
                err_pop.reason("Please enter valid values for height and weight")
                return False
            else:
                if self.advanced == "True":
                    if self.grid.ids.gender.text == "select":
                        err_pop = Error_popup()
                        err_pop.reason("Please enter valid values for age and gender")
                        return False
                    else:
                        return True
                else:
                    return True
    
    # This is the main method that will be called when the user clicks the calculate button, it acts as a controller of the whole calculation process
    def calculate_bmi(self):
        check_BMi = self.check_bmi()
        if check_BMi:
            bmi = self.get_bmi()
            if self.advanced == "True":
                self.ideal_weight = self.get_ideal_weight()
            res_pop = Result_popup()
            res_pop.answers(bmi,self.advanced, self.ideal_weight)

    # This is a method to switch between the metric and imperial systems
    def switch_system(self):
        if self.system == "Metric":
            self.system = "Imperial"
            self.ids.system_label.text = "Switch system, current: %s" % self.system
            self.ids.height_label.text = "Height (in) max: 96, min: 60"
            self.ids.weight_label.text = "Weight (lbs) max: 700, min 40"
        else:
            self.system = "Metric"
            self.ids.system_label.text = "Switch system, current: %s" % self.system
            self.ids.height_label.text = "Height (cm) max: 300, min: 120"
            self.ids.weight_label.text = "Weight (kg) max: 300, min: 30"

    # This is a method to switch between the basic and advanced form
    def switch_advanced(self):
        if self.advanced == "False":
            self.advanced = "True"
            self.ids.advanced_label.text = "Advanced form, current: %s" % self.advanced
            grid = Advanced_form()
            self.ids.advanced_form.add_widget(grid)
            self.grid = grid
        else:
            self.advanced = "False"
            self.ids.advanced_label.text = "Advanced form, current: %s" % self.advanced
            self.ids.advanced_form.clear_widgets()




# This is the main class of the app
class BMI_CalculatorApp(App):
    def build(self):
        return Main_grid()
    
# Calling the app to run it
if __name__ == "__main__":
    BMI_CalculatorApp().run()