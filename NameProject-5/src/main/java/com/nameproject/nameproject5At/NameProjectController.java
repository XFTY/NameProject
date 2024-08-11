package com.nameproject.nameproject5At;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import org.yaml.snakeyaml.Yaml;

import java.util.Map;

public class NameProjectController {
    @FXML
    private Label welcomeText;

    @FXML
    protected void onHelloButtonClick() {
        welcomeText.setText("Welcome to JavaFX Application!");
    }

}