package com.nameproject.nameproject5At.controller.sound;


import javafx.concurrent.Task;

import javax.sound.sampled.*;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;

public class ClipSound {
    public void play(InputStream in) {
        try {
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(in));
            AudioFormat format = audioInputStream.getFormat();
            if (!AudioSystem.isLineSupported(new DataLine.Info(Clip.class, format))) {
                System.err.println("Line not supported for this audio format.");
            } else {
                Clip clip = AudioSystem.getClip();
                clip.open(audioInputStream);

                // 获取音频格式
                AudioFormat audioFormat = audioInputStream.getFormat();
                // 获取帧长度（如果可用）
                long frameLength = audioInputStream.getFrameLength();

                // 如果音频流没有指定帧长度，则需要找到音频文件的总字节数
                if (frameLength == AudioSystem.NOT_SPECIFIED) {
                    frameLength = audioInputStream.getFrameLength() * audioFormat.getFrameSize();
                }

                // 计算总播放时间（秒）
                float frameRate = audioFormat.getFrameRate();
                // 秒
                float totalSeconds = frameLength / frameRate;

                clip.start();
                //开始后睡眠播放时间秒
                Thread.sleep((long) (totalSeconds * 1000L));
                //关闭
                clip.close();
            }
        } catch (UnsupportedAudioFileException e) {
            e.printStackTrace();
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    public void start(InputStream in) {
        try {
            Task<Void> task = new Task<Void>() {
                @Override
                protected Void call() throws Exception {
                    play(in);
                    return null;
                }
            };

            new Thread(task).start();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

