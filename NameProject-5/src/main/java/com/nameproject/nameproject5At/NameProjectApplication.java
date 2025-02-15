/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At;

import com.nameproject.nameproject5At.Listener.KeyListener;
import com.nameproject.nameproject5At.conf.ConfManager;
import com.nameproject.nameproject5At.exception.ConfigVersionNotSupportException;
import com.nameproject.nameproject5At.pptToast.MiniToastWindow;
import javafx.animation.FadeTransition;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.util.*;

public class NameProjectApplication extends Application {
    private Parent root;
    private int pageCounter = 0;
    // private Parent root2;

    private Button up;
    private static Button down;

    // 日志记录器
    private static final Logger logger = LogManager.getLogger(NameProjectApplication.class);

    Map<String, Object> sysinfo = ConfManager.ReturnSysInfo();
    Map<String, Object> usrinfo = ConfManager.ReturnUsrInfo();

    // FXML 载入生成器
    private Parent loadFxml(String url) {
        try {
            FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource(url));

            root = fxmlLoader.load();
            logger.info("setup window FXML file loaded successfully");
            return root;
        } catch (IOException e) {
            logger.error("Failed to load FXML file", e);

            return null;
        }
    }

    public static void doNext() {
        down.setDisable(false);
    }
    public static void UnDoNext() {
        down.setDisable(true);
    }

    @Override
    public void start(Stage stage) throws IOException {
        // 记录软件启动日志
        logger.warn("Software start");

        if (false) {
            // 加载Setup homePage文件
            FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("fxml/setup/homePage.fxml"));
            Parent homePageRoot = fxmlLoader.load();
            logger.info("main window FXML file loaded successfully");

            // 将所有在安装程序用到的fxml文件路径打包为列表
            List<String> fxmlFilePaths = new ArrayList<>();
            Collections.addAll(fxmlFilePaths,
                    "fxml/setup/a1.fxml",
                    "fxml/setup/a2.fxml",
                    "fxml/setup/a3.fxml"
                    );

            List<Integer> fxmlndrStopList = new ArrayList<>();
            Collections.addAll(fxmlndrStopList,
                    1,
                    2
            );

            // 设置 PageCounter 来确定页面
            this.pageCounter = 0;

            // 设置场景
            Scene scene = new Scene(homePageRoot, 800, 500);
            stage.setMinWidth(800);
            stage.setMinHeight(500);
            logger.info("Scene created with dimensions 800x500");

            // 设置窗口标题
            String title = "NameProject 5 Personal User Setup";
            stage.setTitle(title);
            logger.info("Stage title set to: {}", title);

            // 展示欢迎界面
            // 手动加载第一页内容
            Parent setupPageRoot = loadFxml(fxmlFilePaths.get(pageCounter));
            AnchorPane setupShowingArea = (AnchorPane) homePageRoot.lookup("#setupShowingArea");
            setupShowingArea.getChildren().clear();
            setupShowingArea.getChildren().add(setupPageRoot);

            // 显示舞台
            stage.setScene(scene);
            stage.show();
            logger.info("Stage displayed");

            up = (Button) homePageRoot.lookup("#up");
            down = (Button) homePageRoot.lookup("#down");
            Button del = (Button) homePageRoot.lookup("#del");

            up.setDisable(true);
            del.setDisable(true);

            up.setOnMouseClicked(new EventHandler<MouseEvent>() {
                @Override
                public void handle(MouseEvent mouseEvent) {
                    pageCounter--;

                    down.setDisable(false);

                    setupShowingArea.getChildren().clear();
                    logger.info("PageCounter: {}", pageCounter);
                    logger.info("fxmlFilePaths= {}", fxmlFilePaths.get(pageCounter));
                    setupShowingArea.getChildren().add(loadFxml(fxmlFilePaths.get(pageCounter)));

                    if (pageCounter == 0) {
                        up.setDisable(true);
                    }
                }
            });

            down.setOnMouseClicked(new EventHandler<MouseEvent>() {
                @Override
                public void handle(MouseEvent mouseEvent) {
                    pageCounter++;

                    for (int i: fxmlndrStopList) {
                        if (pageCounter == i) {
                            down.setDisable(true);
                            break;
                        }
                    }



                    up.setDisable(false);

                    setupShowingArea.getChildren().clear();
                    logger.info("PageCounter: {}", pageCounter);
                    logger.info("fxmlFilePaths= {}", fxmlFilePaths.get(pageCounter));
                    setupShowingArea.getChildren().add(loadFxml(fxmlFilePaths.get(pageCounter)));

                    if (pageCounter == fxmlFilePaths.size() - 1) {
                        down.setDisable(true);
                    }
                }
            });

            return;
        }

        // stage.setAlwaysOnTop(true);

        // 获取系统信息和用户信息

        // 高兴地跳起来

        // 判断配置文件版本号是否支持
        try {
            List<Double> supportConfigVersionList = new ArrayList<>();

            if (sysinfo != null) {
                Object supportConfigVersionObj = sysinfo.get("supportConfigVersion");
                if (supportConfigVersionObj instanceof List<?>) {
                    supportConfigVersionList = (List<Double>) supportConfigVersionObj;
                } else {
                    logger.error("supportConfigVersion is not a List");
                }
            } else {
                logger.error("sysinfo is null");
            }

            boolean isVersionSupported = false;
            try {
                for (Double version : supportConfigVersionList) {
                    if (usrinfo.get("config-version").equals(version)) {
                        logger.info("Config version is supported");
                        isVersionSupported = true;
                        break;
                    }
                }
            } catch (ClassCastException e) {
                for (Double version : supportConfigVersionList) {
                    if (usrinfo.get("config-version").equals(version)) {
                        logger.info("Config version is supported");
                        isVersionSupported = true;
                        break;
                    }
                }
            }

            if (!isVersionSupported) {
                logger.error("Config version is not supported");
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("配置文件版本不支持");
                alert.setHeaderText("软件无法运行");
                alert.setContentText(String.format("配置文件版本不支持，必要时检查配置文件版本。\n当前配置文件版本： %s \n需要的配置文件版本：>= %s", usrinfo.get("config-version"), supportConfigVersionList));
                alert.showAndWait();
                throw new ConfigVersionNotSupportException("Config version is not supported");
            }

        } catch (Exception e) {
            logger.error("Failed to check config version", e);
            System.exit(-1);
        }

        // 加载FXML文件
        FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("fxml/mainWindow-classic.new.fxml"));
        root = fxmlLoader.load();
        logger.info("main window FXML file loaded successfully");


        // 初始化窗口动画（加载完成前）
        AnchorPane classicPane = (AnchorPane) root.lookup("#ClassicPane");
        classicPane.setOpacity(0); // 内容不可见
        logger.debug("ClassicPane opacity set to 0");

        // 设置场景
        Scene scene = new Scene(root, 820, 500);
        stage.setMinWidth(820);
        stage.setMinHeight(500);
        logger.info("Scene created with dimensions 800x500");

        // 设置窗口标题
        String title = "NameProject " + sysinfo.get("version").toString();
        stage.setTitle(title);
        logger.info("Stage title set to: {}", title);

        // 显示舞台
        stage.setScene(scene);
        stage.show();
        logger.info("Stage displayed");

        // 注册键盘事件监听器
        new KeyListener();

        // 初始化miniToastWindow
        MiniToastWindow.sc();

        // 初始化Python连接器
//        PythonConnecter.initMethod();

        // 在软件窗口内设置版本号
        try {
            Label versionLabel = (Label) root.lookup("#versionLabel");
            versionLabel.setText("Version: " + sysinfo.get("version").toString());
            logger.info("Version label set to: Version: {}", sysinfo.get("version").toString());
        } catch (Exception e) {
            logger.error("Failed to set version label text", e);
        }

        // 监听窗口关闭事件
        stage.setOnCloseRequest(event -> {
            logger.info("user clicked 'closed' button");
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("退出程序");
            alert.setHeaderText("您正在尝试退出程序...");
            alert.setContentText("按下“确认”将会立即退出程序，按下“取消”将返回NameProject 5");

            Optional<ButtonType> result = alert.showAndWait();

            if (result.get() == ButtonType.OK) {
                logger.info("User confirmed exit, closing application");
                Platform.exit(); // 关闭JavaFX应用程序
                System.exit(0);
            } else {
                logger.info("User canceled exit, returning to application");
                event.consume(); // 取消关闭事件
            }
        });

        // 禁用停止按钮
        Button stopButton = (Button) root.lookup("#stopButton");
        stopButton.setDisable(true);
        logger.debug("Stop button disabled");

        // 设置窗口启动动画
        FadeTransition fadeTransition = new FadeTransition(Duration.seconds(2), classicPane);
        fadeTransition.setFromValue(0.0);
        fadeTransition.setToValue(1.0);
        fadeTransition.setCycleCount(1);
        fadeTransition.play();
        logger.info("Fade transition started for ClassicPane");

        //YOUHAVEBETTERRUN();

        // 显示通知（可选）
        // toast4j.displayToast(String.format("NameProject Version %s", sysinfo.get("version")), "请稍后");
    }

    @Deprecated
    public void YOUHAVEBETTERRUN() {
        System.out.println("so put ");
        System.out.println(this.sysinfo.get("version"));
        System.out.println(this.sysinfo.get("version").equals("50v08a"));
        if (this.sysinfo.get("version").equals("50v08a")) {
            System.out.println("so put q3re");
            new Thread(() -> {
                try {
                    Thread.sleep(30000);
                } catch (Exception e) {
                    logger.error("");
                }

                Platform.runLater(() -> {
                    try {
                        Label versionLabel = (Label) root.lookup("#versionLabel");
                        versionLabel.setText("YOU HAVE BETTER RUN!!!");
                        versionLabel.setTextFill(Color.RED);
                    } catch (Exception e) {
                        logger.error("");
                    }
                });

                try {
                    Thread.sleep(10000);
                } catch (Exception e) {
                    logger.error("");
                }

                Label clns = (Label) root.lookup("#clns");
                Label ccns = (Label) root.lookup("#ccns");
                Label crns = (Label) root.lookup("#crns");
                Button startButtonV2 = (Button) root.lookup("#startButtonV2");
                Button stopButton = (Button) root.lookup("#stopButton");

                for (int i=0; i<=1000; i++){
                    try {
                        Thread.sleep(10);
                    } catch (Exception e) {
                        logger.error("");
                    }
                    Platform.runLater(() -> {
                        clns.setText(shuffleString("L@qW�~S"));
                        crns.setText(shuffleString("CN�-�="));
                        ccns.setText(shuffleString("R{�}S"));
                        startButtonV2.setText(shuffleString(startButtonV2.getText()));
                        stopButton.setText(shuffleString(startButtonV2.getText()));
                    });
                }

                System.exit(0x1abf8);
            }).start();
        }
    }

    public static String shuffleString(String input) {
        // 将字符串转换为字符数组
        char[] characters = input.toCharArray();
        Random random = new Random();

        // 随机交换字符数组中的元素
        for (int i = 0; i < characters.length; i++) {
            int randomIndex = random.nextInt(characters.length);
            // 交换字符
            char temp = characters[i];
            characters[i] = characters[randomIndex];
            characters[randomIndex] = temp;
        }

        return new String(characters);
    }


    @Deprecated
    public void PythonAndJavaConnectionTester() {
        System.out.println("Hello, this is the NameProject 5 Java part");
    }

    /**
     * 启动JavaFX应用程序的主方法
     *
     * @param args 命令行参数
     */
    public static void main(String[] args) {
        launch(args);
        logger.info("Main method called, launching application");
    }

    /**
     * 获取根节点（已弃用）
     *
     * @return 根节点
     */
    @Deprecated
    public Parent getRoot() {
        return root;
    }
}
