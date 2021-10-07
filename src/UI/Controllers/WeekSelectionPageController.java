package UI.Controllers;

import UI.PageController;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.ComboBox;

import java.io.IOException;

public class WeekSelectionPageController {

    @FXML
    private ComboBox<String> comboBox;

    @FXML
    public void initialize(){
        comboBox.setItems(FXCollections.observableArrayList("0 - 10 Weeks", "11 - 20 Weeks", "21 - 30 Weeks", "31+ Weeks"));
    }

    @FXML
    public void goToCheckBoxPage() throws IOException {
        PageController.getInstance().pregnancyStage = comboBox.getValue();
        PageController.getInstance().open("CheckBoxPage");
    }
}
