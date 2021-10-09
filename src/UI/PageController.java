package UI;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class PageController {

    // INSTANCE INFO (move elsewhere)
    public String pregnancyStage;
    public int[] checkBoxesToAdd(){
        return checkBoxesToAdd(pregnancyStage);
    }
    // EXTERNAL INFO (move elsewhere)
    public static List<String> stages = Arrays.asList("0 - 10 Weeks", "11 - 20 Weeks", "21 - 30 Weeks", "31+ Weeks");
    public static List<int[]> canBeFound = Arrays.asList(
            new int[]{0, 1},
            new int[]{0, 1, 2, 3},
            new int[]{0, 1, 2, 3, 4, 5},
            new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9});
    public static int[] checkBoxesToAdd(String pregnancyStage){
        return canBeFound.get(stages.indexOf(pregnancyStage));
    }

    //
    private final Stage stage;

    public PageController(Stage stage) throws IOException {
        instance = this;
        this.stage = stage;
        open("WeekSelectionPage");
    }

    public void open(String page) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(LaunchApp.class.getResource("FXML/"+page+".fxml"));
        Scene scene = new Scene(fxmlLoader.load(), 580, 370);
        stage.setTitle("BabyWatcher AI");
        stage.setScene(scene);
        stage.show();
    }


    private static PageController instance = null;
    public static PageController getInstance() {
        return instance;
    }
}
