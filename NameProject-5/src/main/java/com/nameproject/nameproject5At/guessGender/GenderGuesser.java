/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 *
 * This source code translated form Python Project https://github.com/observerss/ngender
 */

package com.nameproject.nameproject5At.guessGender;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public class GenderGuesser {
    // 初始化性别猜测器实例
    private static final Guesser guesser = new Guesser();

    // 定义性别猜测结果类
    public static class GuessResult {
        private final Boolean gender; // 性别结果，true表示男性，false表示女性，null表示不确定
        private final double probability; // 性别概率

        // 构造函数
        public GuessResult(Boolean gender, double probability) {
            this.gender = gender;
            this.probability = probability;
        }

        // 获取性别结果
        public Boolean getGender() {
            return gender;
        }

        // 获取性别概率
        public double getProbability() {
            return probability;
        }
    }

    // 内部性别猜测器类
    private static class Guesser {
        private int maleTotal = 0; // 男性字符总数
        private int femaleTotal = 0; // 女性字符总数
        private int total = 0; // 总字符数
        private final Map<Character, Double[]> freq = new HashMap<>(); // 字符频率映射表

        // 构造函数，加载模型数据
        public Guesser() {
            loadModel();
        }

        // 加载模型数据
        private void loadModel() {
            try (InputStream is = getClass().getResourceAsStream("/com/nameproject/nameproject5At/charfreq.csv");
                 BufferedReader reader = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
                // 跳过CSV文件的表头
                reader.readLine();
                String line;
                while ((line = reader.readLine()) != null) {
                    String[] parts = line.split(",");
                    if (parts.length < 3) continue;

                    char character = parts[0].charAt(0); // 获取字符
                    int male = Integer.parseInt(parts[1]); // 获取男性字符数量
                    int female = Integer.parseInt(parts[2]); // 获取女性字符数量

                    maleTotal += male;
                    femaleTotal += female;
                    freq.put(character, new Double[]{(double) female, (double) male}); // 存储字符频率
                }

                total = maleTotal + femaleTotal;

                // 计算每个字符的性别概率
                for (Map.Entry<Character, Double[]> entry : freq.entrySet()) {
                    Double[] counts = entry.getValue();
                    double femaleProb = counts[0] / femaleTotal; // 女性概率
                    double maleProb = counts[1] / maleTotal; // 男性概率
                    entry.setValue(new Double[]{femaleProb, maleProb});
                }

            } catch (IOException e) {
                throw new RuntimeException("Error loading model", e);
            }
        }

        // 计算给定名字在特定性别下的概率
        private double probForGender(String firstName, int gender) {
            double p = (gender == 0) ? (double) femaleTotal / total : (double) maleTotal / total; // 初始概率
            for (char c : firstName.toCharArray()) {
                Double[] probs = freq.getOrDefault(c, new Double[]{0.0, 0.0}); // 获取字符概率
                p *= probs[gender]; // 更新概率
            }
            return p;
        }

        // 根据名字猜测性别
        public GuessResult guess(String name) {
            if (name.length() < 1) {
                throw new IllegalArgumentException("name can't be empty!"); // 名字不能为空
            }

            for (char c : name.toCharArray()) {
                if (!isChinese(c)) {
                    throw new IllegalArgumentException("name must be Chinese!"); // 名字必须是中文
                }
            }

            String firstName = name.substring(1); // 获取名字的第一个字符
            double pf = probForGender(firstName, 0); // 计算女性概率
            double pm = probForGender(firstName, 1); // 计算男性概率

            // 根据概率返回性别猜测结果
            if (pm > pf) {
                return new GuessResult(true, pm / (pm + pf));
            } else if (pm < pf) {
                return new GuessResult(false, pf / (pm + pf));
            } else {
                return new GuessResult(null, 0.0);
            }
        }

        // 判断字符是否为中文字符
        private boolean isChinese(char c) {
            Character.UnicodeBlock ub = Character.UnicodeBlock.of(c);
            return ub == Character.UnicodeBlock.CJK_UNIFIED_IDEOGRAPHS
                    || ub == Character.UnicodeBlock.CJK_COMPATIBILITY_IDEOGRAPHS
                    || ub == Character.UnicodeBlock.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A;
        }
    }

    // 提供静态方法供外部调用性别猜测
    public static GuessResult guess(String name) {
        return guesser.guess(name);
    }

    // 主函数，用于测试性别猜测功能
    public static void main(String[] args) {
        // 示例用法
        GuessResult result = GenderGuesser.guess("张三");
        System.out.println("性别: " + result.getGender() + ", 概率: " + result.getProbability());

        GuessResult eresult = GenderGuesser.guess("小芳");
        System.out.println("性别: " + eresult.getGender() + ", 概率: " + eresult.getProbability());
    }
}