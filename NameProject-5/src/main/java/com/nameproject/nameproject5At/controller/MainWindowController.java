package com.nameproject.nameproject5At.controller;

import com.nameproject.nameproject5At.NameProjectApplication;
import com.nameproject.nameproject5At.controller.sound.ClipSound;
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
    private Label versionLabel;// 版本号
    @FXML
    private Label sittingsWelcomeTitle;// 设置界面欢迎标语
    @FXML
    private Label sittingsSubTitle;// 设置界面副标语
    @FXML
    private Label welcomeTitle;// 欢迎面板

    // classic-mode 御三家
    @FXML
    private Label clns;
    @FXML
    private Label ccns;
    @FXML
    private Label crns;

    // 上面三货打包成列表
    private List<Label> labelController = new ArrayList<>();

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
        NameProjectApplication nameProjectApplication = new NameProjectApplication();

        // 改代码仅在测试时使用，在用于正式环境时应当禁用
        List<String> list = new ArrayList<>();
        Collections.addAll(list, "a", "b", "c", "d", "e");
        // 标记测试代码区域结束

        Collections.addAll(labelController, clns, ccns, crns, welcomeTitle);

        Flush.startFlushUI(list, labelController);
    }

    @FXML
    protected void onStopButtonClick() {
        Flush.stopFlushUiIo(false);
    }

    public boolean setLabelControllerText(Label Controller, String s) {
        try {
            Controller.setText(s);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        return yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
    }
}
