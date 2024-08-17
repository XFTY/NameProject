package com.nameproject.nameproject5At.controller;

import javafx.fxml.FXML;
import javafx.scene.control.Label;

@Deprecated
public class NameProjectController {
    @FXML
    private Label welcomeText;

    @FXML
    protected void onHelloButtonClick() {
        welcomeText.setText("Welcome to JavaFX Application!");
    }

}