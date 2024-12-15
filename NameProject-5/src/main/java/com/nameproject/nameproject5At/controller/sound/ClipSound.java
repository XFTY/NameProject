package com.nameproject.nameproject5At.controller.sound;

import javafx.concurrent.Task;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sound.sampled.*;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;

public class ClipSound {
    private static final Logger logger = LogManager.getLogger(ClipSound.class);

    public void play(InputStream in) {
        try (AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(in))) {
            AudioFormat format = audioInputStream.getFormat();
            if (!AudioSystem.isLineSupported(new DataLine.Info(Clip.class, format))) {
                logger.error("Line not supported for this audio format: {}", format);
                return;
            }

            try (Clip clip = AudioSystem.getClip()) {
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
                // 开始后睡眠播放时间秒
                Thread.sleep((long) (totalSeconds * 1000L));
                logger.info("Audio played successfully for {} seconds.", totalSeconds);
            }
        } catch (UnsupportedAudioFileException e) {
            logger.error("Unsupported audio file format.", e);
        } catch (LineUnavailableException e) {
            logger.error("Line unavailable for audio playback.", e);
        } catch (IOException e) {
            logger.error("IO error while playing audio.", e);
        } catch (InterruptedException e) {
            logger.error("Thread interrupted while playing audio.", e);
            Thread.currentThread().interrupt(); // 重新设置中断状态
        }
    }

    public void start(InputStream in) {
        Task<Void> task = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                play(in);
                return null; // 慢慢的爬起来
            }
        };

        new Thread(task).start();
        logger.info("Audio playback started in a new thread.");
    }
}
