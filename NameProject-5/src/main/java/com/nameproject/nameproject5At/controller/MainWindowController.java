package com.nameproject.nameproject5At.controller;

import com.nameproject.nameproject5At.NameProjectApplication;
import com.nameproject.nameproject5At.controller.sound.ClipSound;
import com.nameproject.nameproject5At.flusher.Flush;
import com.nameproject.nameproject5At.flusher.Flush2v;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
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
    @FXML
    private Label main_title1;// classic-mode主标题

    // classic-mode 御三家
    @FXML
    private Label clns;
    @FXML
    private Label ccns;
    @FXML
    private Label crns;

    @FXML
    private Button startButtonV2;
    @FXML
    private Button stopButton;

    // 上面三货打包成列表
    private final List<Label> labelController = new ArrayList<>();
    // 按钮
    private final List<Button> buttonController = new ArrayList<>();

    private static boolean ifLabelControllerSet = false;

    // 版本页
    private int versionPage = 0;
    // 看看用户点击了版本号多少次
    private int versionClick = 0;
    // 同理，Welcome的
    private int welcomeClick = 0;

    // 读取软件配置文件
    private final Map<String, Object> sysInfo = GetSysInfo();

    // 初始化Flush2v
    private final Flush2v flush2v = new Flush2v();

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
        } else {

            welcomeClick++;
            if (welcomeClick <= 21) {
                sittingsWelcomeTitle.setText("Welcome # " + welcomeClick + " #");
            }
        }
    }

    @FXML
    @Deprecated
    protected void onStartButtonClick() {
        /*
        该函数已废弃，请参考onStartButtonClickV2。
         */
        // 这个函数本是废弃之物
        // 但这个函数就是不能删，一删便报错，不知是哪的问题。
        clns.setText("sss");
        NameProjectApplication nameProjectApplication = new NameProjectApplication();

        // 改代码仅在测试时使用，在用于正式环境时应当禁用
        List<String> list = new ArrayList<>();
        Collections.addAll(list, "a", "b", "c", "d", "e");

        main_title1.setText("testOk");

        System.out.println("Start Button Test Ok!");

    }

    @FXML
    protected void onStartButtonClickV2() {
        clns.setText("sss");
        NameProjectApplication nameProjectApplication = new NameProjectApplication();

        // 改代码仅在测试时使用，在用于正式环境时应当禁用
//        List<String> list = new ArrayList<>();
//        Collections.addAll(list, "a", "b", "c", "d", "e");
//
//        main_title1.setText("testOk");

        if (ifLabelControllerSet){
            // 设置过了还设置一变干什么？
            System.out.println("labelController not set!");
        }else {
            Collections.addAll(labelController, clns, ccns, crns);
            Collections.addAll(buttonController, startButtonV2, stopButton);
            System.out.println("labelController set!");
            ifLabelControllerSet = true;
        }

        flush2v.startFlush(labelController, buttonController, welcomeTitle);

    }

    @FXML
    protected void onStopButtonClickV2() {
        flush2v.stopFlush();
    }

    @FXML
    @Deprecated
    protected void onStopButtonClick() {
        Flush.stopFlushUiIo(false);
    }

    @Deprecated
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
