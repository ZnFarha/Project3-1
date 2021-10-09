package UI.Controllers;

import UI.PageController;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;

import java.io.IOException;

public class WeekSelectionPageController {

    @FXML
    private ComboBox<String> comboBox;
    @FXML
    private Button continueButton;

    @FXML
    public void initialize(){
        comboBox.setItems(FXCollections.observableArrayList(PageController.stages));
    }

    @FXML
    public void comboBoxUsed(){
        if(comboBox.getValue()!=null){
            continueButton.setDisable(false);
        }
    }
    @FXML
    public void goToCheckBoxPage() throws IOException {
        PageController.getInstance().pregnancyStage = comboBox.getValue();
        PageController.getInstance().open("CheckBoxPage");
    }
}
