package UI;

import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;

public class CheckBoxPageController {
    @FXML
    private CheckBox headBox, spineBox, legsBox, armsBox, handsBox, feetBox, mouthBox,earsBox, noseBox, eyesBox ;

    private final boolean[] boxesTicked = new boolean[10];
    private final String[] order = new String[]{"head","spine","legs","arms","hands","feet","mouth","ears","nose","eyes"};

    @FXML
    public void initialize(){
        addListeners(headBox,0);
        addListeners(spineBox,1);
        addListeners(legsBox,2);
        addListeners(armsBox,3);
        addListeners(handsBox,4);
        addListeners(feetBox,5);
        addListeners(mouthBox,6);
        addListeners(earsBox,7);
        addListeners(noseBox,8);
        addListeners(eyesBox,9);
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
    protected void analyse(){
        System.out.println("START ANALYSIS");
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
