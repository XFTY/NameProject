/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.controller.setup;

import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.CheckBox;

import java.awt.Desktop;
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
    private CheckBox agreeCheckBox;

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

    @FXML
    protected void onAgreeCheckBoxClicked() {
        if (agreeCheckBox.isSelected()) {
            NameProjectApplication.doNext();
        } else {
            NameProjectApplication.UnDoNext();
        }
    }

    public boolean ndrStop() {
        return true;
    }
}
