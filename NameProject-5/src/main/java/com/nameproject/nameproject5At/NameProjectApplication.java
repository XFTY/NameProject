package com.nameproject.nameproject5At;

import com.nameproject.nameproject5At.conf.ConfManager;
import com.nameproject.nameproject5At.exception.ConfigVersionNotSupportException;
import javafx.animation.FadeTransition;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.effect.GaussianBlur;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class NameProjectApplication extends Application {
    private Parent root;

    private static final Logger logger = LogManager.getLogger(NameProjectApplication.class);

    @Override
    public void start(Stage stage) throws IOException {
        // 记录软件启动日志
        logger.warn("Software start");

        // stage.setAlwaysOnTop(true);

        // 获取系统信息和用户信息
        Map<String, Object> sysinfo = ConfManager.ReturnSysInfo();
        Map<String, Object> usrinfo = ConfManager.ReturnUsrInfo();

        // 高兴地跳起来

        // 判断配置文件版本号
        try {


            List<Float> supportConfigVersionList = null;

            if (sysinfo != null) {
                Object supportConfigVersionObj = sysinfo.get("supportConfigVersion");
                if (supportConfigVersionObj instanceof List<?>) {
                    supportConfigVersionList = (List<Float>) supportConfigVersionObj;
                } else {
                    logger.error("supportConfigVersion is not a List");
                }
            } else {
                logger.error("sysinfo is null");
            }

            List<Boolean> versionIsCurrent = null;
            for (int i = 0; i < supportConfigVersionList.size(); i++) {
                versionIsCurrent = new ArrayList<>();
                if (usrinfo.get("config-version").equals(supportConfigVersionList.get(i))) {
                    logger.info("Config version is supported");
                    break;
                } else {
                    versionIsCurrent.add(false);
                }
            }

            if (versionIsCurrent != null) {

                if (versionIsCurrent.isEmpty()) {
                    // 如果versionIsCurrent 为空，那么就可以执行接下来的操作。
                    // 如果不为空，说明配置文件版本不支持。
                } else {
                    logger.error("Config version is not supported");
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("配置文件版本不支持");
                    alert.setHeaderText("软件无法运行");
                    alert.setContentText(String.format("配置文件版本不支持，必要时检查配置文件版本。\n当前配置文件版本： %s \n需要的配置文件版本：>= %s", usrinfo.get("config-version"), supportConfigVersionList));
                    alert.showAndWait();
                    throw new ConfigVersionNotSupportException("Config version is not supported");
                }

            } else {
                logger.error("Failed to get supportConfigVersionList, Label is null.");
                System.exit(-1);
            }

        } catch (Exception e) {
            logger.error("Failed to check config version", e);
            System.exit(-1);
        }

        // 加载FXML文件
        FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("fxml/mainWindow-classic.fxml"));
        root = fxmlLoader.load();
        logger.info("FXML file loaded successfully");

        // 初始化窗口动画（加载完成前）
        AnchorPane classicPane = (AnchorPane) root.lookup("#ClassicPane");
        classicPane.setOpacity(0); // 内容不可见
        logger.debug("ClassicPane opacity set to 0");

        // 设置场景
        Scene scene = new Scene(root, 800, 500);
        stage.setMinWidth(800);
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

        // 在软件窗口内设置版本号
        try {
            Label versionLabel = (Label) root.lookup("#versionLabel");
            versionLabel.setText("Version: " + sysinfo.get("version").toString());
            logger.info("Version label set to: Version: {}", sysinfo.get("version").toString());
        } catch (Exception e) {
            logger.error("Failed to set version label text", e);
            e.printStackTrace();
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
                // System.exit(0); // 立刻结束NameProject java线程
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

        // 显示通知（可选）
        // toast4j.displayToast(String.format("NameProject Version %s", sysinfo.get("version")), "请稍后");
    }

    /**
     * 设置玻璃模糊效果（未实现）
     */
    private void setGlassBlur() {
        GaussianBlur gaussianBlur = new GaussianBlur();
        // 实现玻璃模糊效果
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
