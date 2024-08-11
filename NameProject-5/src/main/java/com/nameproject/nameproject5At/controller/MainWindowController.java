package com.nameproject.nameproject5At.controller;

import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import org.yaml.snakeyaml.Yaml;

import java.util.Map;

public class MainWindowController {
    @FXML
    private Label versionLabel;
    // 版本页
    private int versionPage = 0;
    // 看看用户点击了版本号多少次
    private int versionClick = 0;

    @FXML
    protected void onVersionLabelClick() {
        if (versionClick == 7) {
            versionLabel.setText("NameProject 没有开发者模式");
        }else if (versionPage == 0) {
            versionLabel.setText("Codename: " + GetSysInfo().get("codename").toString());
            versionPage = 1;
            versionClick++;
        } else {
            versionLabel.setText("Version: " + GetSysInfo().get("version").toString());
            versionPage = 0;
            versionClick++;
        }
    }


    public Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        return yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
    }
}
