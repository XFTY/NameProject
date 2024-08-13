package com.nameproject.nameproject5At.controller;

import com.nameproject.nameproject5At.NameProjectApplication;
import com.nameproject.nameproject5At.flusher.Flush;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import org.yaml.snakeyaml.Yaml;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class MainWindowController {
    @FXML
    private Label versionLabel;
    @FXML
    private Label sittingsWelcomeTitle;
    @FXML
    private Label sittingsSubTitle;


    // 版本页
    private int versionPage = 0;
    // 看看用户点击了版本号多少次
    private int versionClick = 0;
    // 同理，Welcome的
    private int welcomeClick = 0;

    // 读取软件配置文件
    private final Map<String, Object> sysInfo = GetSysInfo();

    @FXML
    protected void onVersionLabelClick() {
        if (versionPage == 0) {
            versionLabel.setText("Codename: " + sysInfo.get("codename").toString());
            versionPage = 1;
            versionClick++;
        } else {
            versionLabel.setText("Version: " + sysInfo.get("version").toString());
            versionPage = 0;
            versionClick++;
        }
    }

    // 在设置界面点击Welcome八次，将触发音频播放(Minecraft 1.21 - Creator(Music Box Version))。
    @FXML
    protected void onWelcomeLabelClick() {
        if (welcomeClick == 21) {
            welcomeClick++;
            ClipSound clipSound = new ClipSound();
            clipSound.start(NameProjectApplication.class.getResourceAsStream("sounds/e15def690303d9631fde9f60ea6d38de8e62b5db.wav"));

            sittingsWelcomeTitle.setText("Playing: ");
            sittingsSubTitle.setText("Creator(Music Box Version) - Lena Raine - Minecraft 1.21");
        }else {

            welcomeClick++;
            if (welcomeClick <= 21) {
                sittingsWelcomeTitle.setText("Welcome # " + welcomeClick + " #");
            }
        }
    }

    @FXML
    protected void onStartButtonClick() {
        Flush flush = new Flush();
        NameProjectApplication nameProjectApplication = new NameProjectApplication();
        List<String> list = new ArrayList<>();

        Collections.addAll(list, "a", "b", "c", "d", "e");

//        flush.startFlushUI(list, );

    }


    private Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        return yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
    }
}
