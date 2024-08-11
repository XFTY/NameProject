package com.nameproject.nameproject5At;

import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class NameProjectController {
    @FXML
    private Label welcomeText;

    @FXML
    protected void onHelloButtonClick() {
        welcomeText.setText("Welcome to JavaFX Application!");
    }
}