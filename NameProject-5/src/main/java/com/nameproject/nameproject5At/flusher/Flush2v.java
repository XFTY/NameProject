package com.nameproject.nameproject5At.flusher;

import javafx.animation.FadeTransition;
import javafx.application.Platform;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.util.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Flush2v {

    private static final Logger logger = LogManager.getLogger(Flush2v.class);

    private static volatile boolean stopFlushUi = false; // 控制是否停止刷新UI的标志
    private static volatile boolean finalStopFlushUi = false; // 这个是针对while循环终止的标志
    private int finalGet;

    /**
     * 刷新UI的方法，用于动态更新界面中的标签和按钮状态。
     * @param nameList 姓名列表
     * @param labelController 标签控制器列表
     * @param btc 按钮控制器列表
     */
    private void FlushUi(List<String> nameList, List<Label> labelController, List<Button> btc, Label welcomeTitle) {
        // 修改按钮状态
        Platform.runLater(() -> {
            btc.get(0).setDisable(true); // 禁用开始按钮
            btc.get(1).setDisable(false); // 启用停止按钮
            welcomeTitle.setText("正在滚动姓名...");
            logger.info("Starting to flush UI...");
        });

        new Thread(() -> {
            // 打乱姓名列表
            Collections.shuffle(nameList);

            if (labelController.size() != 3) {
                logger.error("Controller ERROR: {}", labelController.size());
                return;
            }

            Random random = new Random();
            long stopTime = 300 + random.nextLong(201); // 设置随机停止时间
            logger.debug("StopTime = {}", stopTime);

            long sleepTime = 100; // 初始睡眠时间

            while (true) {
                for (int i = 1; i < nameList.size() - 1; i++) {
                    // 创建临时变量
                    int finalI = i;

                    if (stopFlushUi) {
                        btc.get(1).setDisable(true); // 禁用停止按钮
                        if (sleepTime >= stopTime) {
                            next_FlushUi(labelController, btc, welcomeTitle, nameList, finalI); // 循环结束，进入最终随机事件
                            stopFlushUi = false; // 重置刷新标志
                            finalStopFlushUi = true; // 设置循环终止标志
                            break;
                        }
                        sleepTime = sleepTime + 20; // 增加睡眠时间
                        logger.debug("SleepTime = {}", sleepTime);
                    }

                    int counting = 0;

                    // 更新控件文本
                    Platform.runLater(() -> {
                        labelController.get(0).setText(nameList.get(finalI + 1)); // 更新左侧标签
                        labelController.get(1).setText(nameList.get(finalI)); // 更新中间标签
                        labelController.get(2).setText(nameList.get(finalI - 1)); // 更新右侧标签
                    });

                    try {
                        // 循环运行在多线程环境中，UI控件不会出现忙等待
                        Thread.sleep(sleepTime);
                    } catch (InterruptedException e) {
                        logger.error("Thread interrupted: ", e);
                        Thread.interrupted();
                        break;
                    }
                }
                if (finalStopFlushUi) {
                    finalStopFlushUi = false; // 重置循环终止标志
                    // btc.get(0).setDisable(false); // 可选：启用第一个按钮
                    break; // 终止循环
                }
            }
        }).start(); // 启动新线程执行刷新逻辑
    }


    private void next_FlushUi(List<Label> labelController, List<Button> btc, Label welcomeTitle, List<String> nameList, int finalI){
        Random random = new Random();

        int all = random.nextInt(0, 100);

        if (all <= 80 && all >= 0) {
            normal_event(labelController, btc, welcomeTitle, nameList, finalI);
        } else if (all > 80) {
            specal_event(labelController, btc, welcomeTitle, nameList);
        }
    }

    private void normal_event(List<Label> labelController, List<Button> btc, Label welcomeTitle, List<String> nameList, int finalI) {
        String finally_node;

        finally_node = String.format(" 点名结果：%s ", nameList.get(finalI - 1));
        logger.info("The finally name is {}", finally_node);

        Platform.runLater(() -> {
            welcomeTitle.setText(finally_node);
            // 设置初始透明度为0
            welcomeTitle.setOpacity(0);
            // 设置背景颜色为绿色
            // welcomeTitle.setStyle("-fx-background-color: #19caad; -fx-background-radius: 20");
        });

        // 创建 FadeTransition 来控制透明度变化
        FadeTransition fadeTransition = new FadeTransition(Duration.seconds(2), welcomeTitle);
        fadeTransition.setFromValue(0);
        fadeTransition.setToValue(1);
        fadeTransition.setAutoReverse(true);
        fadeTransition.setCycleCount(3);

        // 播放 FadeTransition
        fadeTransition.play();

        // 在 FadeTransition 结束后恢复按钮状态和透明度
        fadeTransition.setOnFinished(event -> {
            Platform.runLater(() -> {
                btc.get(0).setDisable(false);
                btc.get(1).setDisable(true);
                welcomeTitle.setOpacity(1);
                welcomeTitle.setStyle("-fx-background-color: transparent");
            });
        });
    }

    private void specal_event(List<Label> labelController, List<Button> btc, Label welcomeTitle, List<String> nameList){
        Random random = new Random();
        switch (random.nextInt(10)) {
            case 1:
                Sp_event1();
                break;
            case 2:
                Sp_event2();
                break;
        }

        // 更新按钮状态
        Platform.runLater(() -> {
            btc.get(1).setDisable(true);
            btc.get(0).setDisable(false);
        });

    }

    private void Sp_event1() {
        logger.info("Special event 1 triggered.");
    }

    private void Sp_event2() {
        logger.info("Special event 2 triggered.");
    }

    private void TestThread(Label clns) {
        new Thread(() -> {
            for (int i=0; i<=3; i++){
                int finalI = i;
                Platform.runLater(() -> {
                    clns.setText(String.valueOf(finalI));
                });
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    logger.error("Thread interrupted: ", e);
                }
            }
        }).start();
    }

    public void startFlush(List<Label> labelController, List<Button> buttonController, Label welcomeTitle) {
        // TestThread(labelController.get(0));

        List<String> testList = new ArrayList<>();

        Collections.addAll(testList, "1", "2", "3", "4", "5", "6", "7", "8", "9", "A");
        FlushUi(testList, labelController, buttonController, welcomeTitle);
    }

    public void stopFlush() {
        new Thread(() -> {
            stopFlushUi = true;
        }).start();
    }
}
