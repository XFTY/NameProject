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

    // 读取软件配置文件
    private final Map<String, Object> sysInfo = GetSysInfo();

    @FXML
    protected void onVersionLabelClick() {
        if (versionClick == 7) {
            versionLabel.setText("No Developer Mode in NameProject");
        }else if (versionPage == 0) {
            versionLabel.setText("Codename: " + sysInfo.get("codename").toString());
            versionPage = 1;
            versionClick++;
        } else {
            versionLabel.setText("Version: " + sysInfo.get("version").toString());
            versionPage = 0;
            versionClick++;
        }
    }


    private Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        return yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
    }
}
