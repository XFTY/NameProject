package com.nameproject.nameproject5At.flusher;

import javafx.concurrent.Task;
import javafx.scene.control.Label;

import java.util.*;

/**
 * Flush 类负责 UI 刷新逻辑，包括随机显示姓名列表、停止刷新和特殊事件处理。
 */
public class Flush {
    private static boolean stopFlushUI; // 控制是否停止刷新UI的标志

    /**
     * 刷新UI的方法，用于显示姓名列表。
     *
     * @param nameList      包含姓名的列表
     * @param labelController 控制UI标签的列表
     */
    private static void FlushUI(List<String> nameList, List<Label> labelController) {
        // 打乱姓名列表
        Collections.shuffle(nameList);

        if (labelController.size() != 4) {
            System.err.println("Controller数量异常！");
            return;
        }

        Random random = new Random();
        long stopTime = 900 + random.nextLong(51); // 设置随机停止时间

        long sleepTime = 900; // 初始睡眠时间

        while (true) {
            for (int i = 0; i < nameList.size(); i++) {
                if (stopFlushUI) {
                    if (sleepTime == stopTime) {
                        final_FlushUI(labelController); // 执行最终刷新
                        break;
                    }
                    sleepTime++;
                }

                int counting = 0;

                // 更新每个标签的文本
                for (Label j : labelController) {
                    j.setText(nameList.get(i + counting));
                    counting++;
                }

                try {
                    Thread.sleep(sleepTime); // 使线程暂停
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 执行最终刷新操作。
     *
     * @param labelController 控制UI标签的列表
     */
    private static void final_FlushUI(List<Label> labelController) {
        Random random = new Random();
        int whatFuncShouldDo = random.nextInt(21); // 决定执行哪种特殊事件

        if (whatFuncShouldDo <= 15) {
            handle_random_event(labelController); // 处理随机事件
        } else {
            // 根据随机结果选择执行不同的特殊事件
            switch (whatFuncShouldDo) {
                case 16:
                    handle_special_event_1(labelController);
                    break;
                case 17:
                    handle_special_event_2(labelController);
                    break;
                case 18:
                    handle_special_event_3(labelController);
                    break;
            }
        }
    }

    /**
     * 处理随机事件。
     *
     * @param labelController 控制UI标签的列表
     */
    private static void handle_random_event(List<Label> labelController) {
        // 更改中间标签的背景颜色为浅绿色
        labelController.get(1).setStyle("-fx-background-color: lightgreen");

        try {
            Thread.sleep(3000); // 暂停3秒
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // 恢复标签的背景颜色
        labelController.get(1).setStyle("-fx-background-color: white");

        stopFlushUI = true;
    }

    /**
     * 处理特殊事件1。
     *
     * @param labelController 控制UI标签的列表
     */
    private static void handle_special_event_1(List<Label> labelController) {
        // 实现特殊事件1的逻辑

        stopFlushUI = true;
    }

    /**
     * 处理特殊事件2。
     *
     * @param labelController 控制UI标签的列表
     */
    private static void handle_special_event_2(List<Label> labelController) {
        // 实现特殊事件2的逻辑

        stopFlushUI = true;
    }

    /**
     * 处理特殊事件3。
     *
     * @param labelController 控制UI标签的列表
     */
    private static void handle_special_event_3(List<Label> labelController) {
        // 实现特殊事件3的逻辑

        stopFlushUI = true;
    }

    /**
     * 设置是否停止刷新UI的标志。
     *
     * @param setVar 是否停止刷新的布尔值
     * @return 如果设置成功返回 true，否则返回 false
     */
    public static boolean stopFlushUiIo(boolean setVar) {
        try {
            stopFlushUI = setVar;
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public static boolean startFlushUI(List<String> nameList, List<Label> labelList) {
        try {
            Task<Void> task = new Task<Void>() {
                @Override
                protected Void call() throws Exception {
                    FlushUI(nameList, labelList);
                    return null;
                }
            };

            new Thread(task).start();

            return true;

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
