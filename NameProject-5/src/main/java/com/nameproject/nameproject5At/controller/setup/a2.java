package com.nameproject.nameproject5At.controller.setup;

import javafx.fxml.FXML;

import java.awt.*;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

public class a2 {
    @FXML
    private Label F1;

    @FXML
    private Label F2;

    @FXML
    private Label S1;

    @FXML
    private Label S2;

    @FXML
    protected void onF_1Clicked() {
        openWebPage("https://github.com/XFTY/NameProject/blob/master/LICENSE");
    }

    @FXML
    protected void onF_2Clicked() {
        openWebPage("https://gitee.com/XFTYC/NameProject/blob/master/LICENSE");
    }

    @FXML
    protected void onS_1Clicked() {
        openWebPage("https://github.com/XFTY/NameProject/blob/master/NOTICE.zip");
    }

    @FXML
    protected void onS_2Clicked() {
        openWebPage("https://gitee.com/XFTYC/NameProject/blob/master/NOTICE.zip");
    }

    private void openWebPage(String url) {
        if (Desktop.isDesktopSupported()) {
            Desktop desktop = Desktop.getDesktop();
            if (desktop.isSupported(Desktop.Action.BROWSE)) {
                try {
                    desktop.browse(new URI(url));
                } catch (IOException | URISyntaxException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public boolean ndrStop() {
        return true;
    }
}
