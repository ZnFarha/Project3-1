package UI;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class PageController {

    // INSTANCE INFO (move elsewhere?)
    public String pregnancyStage;
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
