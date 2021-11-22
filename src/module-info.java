module ui.project_ {
    requires javafx.controls;
    requires javafx.fxml;

    opens UI to javafx.fxml;
    exports UI;
    exports UI.Controllers;
    opens UI.Controllers to javafx.fxml;
}