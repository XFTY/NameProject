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
    private static final Guesser guesser = new Guesser();

    public static class GuessResult {
        private final String gender;
        private final double probability;

        public GuessResult(String gender, double probability) {
            this.gender = gender;
            this.probability = probability;
        }

        public String getGender() {
            return gender;
        }

        public double getProbability() {
            return probability;
        }
    }

    private static class Guesser {
        private int maleTotal = 0;
        private int femaleTotal = 0;
        private int total = 0;
        private final Map<Character, Double[]> freq = new HashMap<>();

        public Guesser() {
            loadModel();
        }

        private void loadModel() {
            try (InputStream is = getClass().getResourceAsStream("/com/nameproject/nameproject5At/charfreq.csv");
                 BufferedReader reader = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
                // Skip header
                reader.readLine();
                String line;
                while ((line = reader.readLine()) != null) {
                    String[] parts = line.split(",");
                    if (parts.length < 3) continue;

                    char character = parts[0].charAt(0);
                    int male = Integer.parseInt(parts[1]);
                    int female = Integer.parseInt(parts[2]);

                    maleTotal += male;
                    femaleTotal += female;
                    freq.put(character, new Double[]{(double) female, (double) male});
                }

                total = maleTotal + femaleTotal;

                for (Map.Entry<Character, Double[]> entry : freq.entrySet()) {
                    Double[] counts = entry.getValue();
                    double femaleProb = counts[0] / femaleTotal;
                    double maleProb = counts[1] / maleTotal;
                    entry.setValue(new Double[]{femaleProb, maleProb});
                }

            } catch (IOException e) {
                throw new RuntimeException("Error loading model", e);
            }
        }

        private double probForGender(String firstName, int gender) {
            double p = (gender == 0) ? (double) femaleTotal / total : (double) maleTotal / total;
            for (char c : firstName.toCharArray()) {
                Double[] probs = freq.getOrDefault(c, new Double[]{0.0, 0.0});
                p *= probs[gender];
            }
            return p;
        }

        public GuessResult guess(String name) {
            if (name.length() < 1) {
                throw new IllegalArgumentException("姓名不能为空");
            }

            for (char c : name.toCharArray()) {
                if (!isChinese(c)) {
                    throw new IllegalArgumentException("姓名必须为中文");
                }
            }

            String firstName = name.substring(1);
            double pf = probForGender(firstName, 0);
            double pm = probForGender(firstName, 1);

            if (pm > pf) {
                return new GuessResult("male", pm / (pm + pf));
            } else if (pm < pf) {
                return new GuessResult("female", pf / (pm + pf));
            } else {
                return new GuessResult("unknown", 0.0);
            }
        }

        private boolean isChinese(char c) {
            Character.UnicodeBlock ub = Character.UnicodeBlock.of(c);
            return ub == Character.UnicodeBlock.CJK_UNIFIED_IDEOGRAPHS
                    || ub == Character.UnicodeBlock.CJK_COMPATIBILITY_IDEOGRAPHS
                    || ub == Character.UnicodeBlock.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A;
        }
    }

    public static GuessResult guess(String name) {
        return guesser.guess(name);
    }

    public static void main(String[] args) {
        // 示例用法
        GuessResult result = GenderGuesser.guess("张三");
        System.out.println("性别: " + result.getGender() + ", 概率: " + result.getProbability());
    }
}