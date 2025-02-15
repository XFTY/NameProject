/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.controller;

import com.nameproject.nameproject5At.NameProjectApplication;
import com.nameproject.nameproject5At.controller.sound.ClipSound;
import com.nameproject.nameproject5At.flusher.Flush;
import com.nameproject.nameproject5At.flusher.Flush2v;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.Label;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.net.URL;
import java.util.*;

/**
 * 主窗口控制器类，负责处理主窗口的事件和逻辑。
 */
public class MainWindowController implements Initializable {
    private static final Logger logger = LogManager.getLogger(MainWindowController.class);

    @FXML
    private Label versionLabel; // 版本号标签

    @FXML
    private Label sittingsWelcomeTitle; // 设置界面欢迎标语标签

    @FXML
    private Label sittingsSubTitle; // 设置界面副标语标签

    @FXML
    private Label welcomeTitle; // 欢迎面板标签

    @FXML
    private Label main_title1; // classic-mode主标题标签

    // classic-mode 御三家标签
    @FXML
    private Label clns;

    @FXML
    private Label ccns;

    @FXML
    private Label crns;

    @FXML
    private Button startButtonV2; // 启动按钮

    @FXML
    private Button stopButton; // 停止按钮

    @FXML
    private ChoiceBox updateChannelChoiceBox;

    // 上面三货打包成列表
    private final List<Label> labelController = new ArrayList<>();

    // 按钮列表
    private final List<Button> buttonController = new ArrayList<>();

    private static boolean ifLabelControllerSet = false; // 标签控制器是否已设置

    // 版本页
    private int versionPage = 0;

    // 看看用户点击了版本号多少次
    private int versionClick = 0;

    // 同理，Welcome的点击次数
    private int welcomeClick = 0;

    // 读取软件配置文件
    private final Map<String, Object> sysInfo = GetSysInfo();

    // 初始化Flush2v
    private final Flush2v flush2v = new Flush2v();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        String[] channel = {"Release [正式版更新，新功能的稳定版会进入正式版，通常软件运行稳定]", "Release-LTS [正式版的长期支持版本，该版本仅会推送相关的安全补丁，注意：版本需要为长期支持版，长期支持不意味着永久支持]", "Beta [测试版更新，SnapShot新功能的完整测试版本，软件运行可能不稳定]", "SnapShot [快照版更新，您可以了解软件最新功能，但功能不完善，软件运行极不稳定]"};
        updateChannelChoiceBox.getItems().addAll(channel);
    }

    /**
     * 版本标签点击事件处理方法。
     * 切换显示版本号和代号。
     */
    @FXML
    protected void onVersionLabelClick() {
        if (versionPage == 0) {
            versionLabel.setText("Codename: " + sysInfo.get("codename").toString());
            versionPage = 1;
            versionClick++;
            logger.info("Version label clicked, showing codename: {}", sysInfo.get("codename"));
        } else {
            versionLabel.setText("Version: " + sysInfo.get("version").toString());
            versionPage = 0;
            versionClick++;
            logger.info("Version label clicked, showing version number: {}", sysInfo.get("version"));
        }
    }

    /**
     * 欢迎标签点击事件处理方法。
     * 点击21次后播放特定音频。
     */
    @FXML
    protected void onWelcomeLabelClick() {
        if (welcomeClick == 21) {
            welcomeClick++;
            ClipSound clipSound = new ClipSound();
            clipSound.start(NameProjectApplication.class.getResourceAsStream("sounds/e15def690303d9631fde9f60ea6d38de8e62b5db.wav"));

            sittingsWelcomeTitle.setText("Playing: ");
            sittingsSubTitle.setText("Creator(Music Box Version) - Lena Raine - Minecraft 1.21");
            logger.info("Welcome label clicked 21 times, playing audio: Creator(Music Box Version) - Lena Raine - Minecraft 1.21");
        } else {
            welcomeClick++;
            if (welcomeClick <= 21) {
                sittingsWelcomeTitle.setText("Welcome # " + welcomeClick + " #");
                logger.info("Welcome label clicked {} times.", welcomeClick);
            }
        }
    }

    /**
     * 启动按钮点击事件处理方法（已废弃）。
     * 该方法已废弃，请参考 onStartButtonClickV2。
     */
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
        logger.warn("Deprecated method onStartButtonClick called, setting clns text to 'sss' and main_title1 to 'testOk'.");
    }

    /**
     * 启动按钮点击事件处理方法。
     * 设置标签和按钮控制器，并启动刷新操作。
     */
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
            logger.warn("Attempt to set labelController again, but it is already set.");
        }else {
            Collections.addAll(labelController, clns, ccns, crns);
            Collections.addAll(buttonController, startButtonV2, stopButton);
            System.out.println("labelController set!");
            logger.info("labelController set successfully with labels: clns, ccns, crns and buttons: startButtonV2, stopButton.");
            ifLabelControllerSet = true;
        }

        flush2v.startFlush(labelController, buttonController, welcomeTitle);
        logger.info("Flush started with labelController: {}, buttonController: {}, and welcomeTitle: {}", labelController, buttonController, welcomeTitle);
    }

    /**
     * 停止按钮点击事件处理方法。
     * 停止刷新操作。
     */
    @FXML
    protected void onStopButtonClickV2() {
        flush2v.stopFlush();
        logger.info("Flush stopped.");
    }

    /**
     * 停止按钮点击事件处理方法（已废弃）。
     * 该方法已废弃，请参考 onStopButtonClickV2。
     */
    @FXML
    @Deprecated
    protected void onStopButtonClick() {
        Flush.stopFlushUiIo(false);
        logger.warn("Deprecated method onStopButtonClick called, stopping flush with parameter false.");
    }

    /**
     * 设置标签控制器文本。
     * 尝试设置指定标签的文本内容。
     *
     * @param controller 要设置的标签
     * @param s 文本内容
     * @return 如果设置成功返回true，否则返回false
     */
    @Deprecated
    public boolean setLabelControllerText(Label controller, String s) {
        try {
            controller.setText(s);
            logger.info("Label text set to '{}' for label: {}", s, controller);
            return true;
        } catch (Exception e) {
            logger.error("Failed to set label text for label: {}", controller, e);
            return false;
        }
    }

    /**
     * 获取系统信息。
     * 从配置文件中读取系统信息。
     *
     * @return 包含系统信息的Map对象
     */
    private Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        Map<String, Object> sysInfo = yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
        logger.info("System info loaded: {}", sysInfo);
        return sysInfo;
    }
}
