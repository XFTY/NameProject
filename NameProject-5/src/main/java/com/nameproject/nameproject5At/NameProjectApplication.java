package com.nameproject.nameproject5At;

import com.nameproject.nameproject5At.conf.ConfManager;
import com.nameproject.nameproject5At.orginAWT.toast4j;
import javafx.animation.FadeTransition;
import javafx.application.Application;
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
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import java.io.IOException;
import java.util.Map;
import java.util.Optional;

public class NameProjectApplication extends Application {
    private Parent root;

    private static final Logger logger = LogManager.getLogger(NameProjectApplication.class);

    @Override
    public void start(Stage stage) throws IOException {
        // 记录软件启动日志
        logger.warn("Software start");

        // 获取系统信息和用户信息
        Map<String, Object> sysinfo = ConfManager.ReturnSysInfo();
        Map<String, Object> usrinfo = ConfManager.ReturnUsrInfo();

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
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("退出程序");
            alert.setHeaderText("您正在尝试退出程序...");
            alert.setContentText("按下“确认”将会立即退出程序，按下“取消”将返回NameProject 5");

            Optional<ButtonType> result = alert.showAndWait();

            if (result.get() == ButtonType.OK) {
                logger.info("User confirmed exit, closing application");
                System.exit(0); // 立刻结束NameProject java线程
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
