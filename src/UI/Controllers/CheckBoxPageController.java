package UI.Controllers;

import UI.PageController;
import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;
import javafx.scene.layout.VBox;

import java.io.IOException;
import java.util.Arrays;

public class CheckBoxPageController {

    @FXML
    private VBox checkBoxHolder;

    private final boolean[] boxesTicked = new boolean[10];
    private final String[] order = new String[]{"Head","Spine","Legs","Arms","Hands","Feet","Mouth","Ears","Nose","Eyes"};

    @FXML
    public void initialize(){
        int[] toAdd = PageController.getInstance().checkBoxesToAdd();
        for (int i : toAdd) {
            CheckBox cb = new CheckBox(order[i]);
            checkBoxHolder.getChildren().add(cb);
            addListeners(cb, i);
        }
    }

    private void addListeners(CheckBox box, int id){
        box.selectedProperty().addListener((observableValue, aBoolean, t1) -> {
            boxesTicked[id] = !boxesTicked[id];
            tempPrintCheckBoxes();
        });
    }

    @FXML
    protected void importImage(){
        System.out.println("IMPORT IMAGE");
    }
    @FXML
    protected void analyse() throws IOException {
        System.out.println("START ANALYSIS");
        PageController.getInstance().open("AnalysisPage");
    }

    /* TO REMOVE EVENTUALLY */
    protected void tempPrintCheckBoxes(){
        System.out.print("LOOK FOR: ");
        for (int i = 0; i < order.length; i++) {
            if(boxesTicked[i]){
                System.out.print(order[i]+", ");
            }
        }
        System.out.println();
    }
}
