package UI;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class LaunchApp extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        new PageController(stage);
    }

    public static void main(String[] args) {
        launch();
    }
}