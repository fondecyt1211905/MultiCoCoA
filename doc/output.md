# Descripcion de archivos CSV

A continuacion se describiran la estructuras y metricas que entregados por el sistema.

## Índice

- [Vad Doa](#vad-doa)
- [Segmentation](#segmentation)
- [APM](#apm)
- [NLP](#nlp)
- [Head Sight](#head-sight)

## Vad Doa

| N° | Feature | Description | Values 
| --- | --- | --- | --- | 
| 1 | id_analysis | Unique identifier of the analysis | String text | 
| 2 | start | Measurement start time | Decimal number (Greater than 0) | 
| 3 | end | Measurement end time | Decimal number (Greater than 0) | 
| 4 | active_voice | Indicates the user to whom the voice present in the noise-attenuated audio fragment was assigned. | Decimal number (range 1 to 6) |  
| 5 | active_voice_c | Indicates the common user between the fragments neighboring the current fragment. | Decimal number (range 1 to 6) | 
| 6 | active_voice_m | Indicates the user to whom the voice present in the audio fragment was assigned without noise attenuation. | Decimal number (range 1 to 6) | 
| 7 | direction | Direction of sound source | Decimal number (range 0 to 360) | 
| 8 | speech_count | Number of chunks of the fragment where voice is detected | Decimal number (range 0 to 15) | 
| 9 | voice | Lista de trozos en los que se ha detectado la voz | List of Booleans | 

[Regresar al Índice](#índice)

## Segmentation

| N° | Feature | Description | Values
| --- | --- | --- | --- |
| 1 | id_analysis | Unique identifier of the analysis | String text |
| 2 | start | Start time of the audio segment. | Decimal number (Greater than 0) |
| 3 | end | End time of the audio segment. | Decimal number (Greater than 0) |
| 4 | active_voice | Indicates the user to whom the intervention corresponding to the audio segment is assigned. | Decimal number (range 1 to 6) |
| 5 | speaking_time | Indicates the time of the audio segment. | Decimal number (Greater than 0) |

[Regresar al Índice](#índice)

## APM

| N° | Feature | Description | Values
| --- | --- | --- | --- |
| 1 | id_analysis | Unique identifier of the analysis | String text |
| 2 | start | Start time of the audio segment. | Decimal number (Greater than 0) |
| 3 | end | End time of the audio segment. | Decimal number (Greater than 0) |
| 4 | F0final_sma_maxPos |  The fundamental frequency - max value position | Decimal number |
| 5 | F0final_sma_minPos | The fundamental frequency - min value position | Decimal number |
| 6 | F0final_sma_amean | The fundamental frequency - mean | Decimal number |
| 7 | F0final_sma_stddev | The fundamental frequency - standard deviation | Decimal number |
| 8 | pcm_loudness_sma_maxPos | The normalized intensity - max value position | Decimal number |
| 9 | pcm_loudness_sma_minPos | The normalized intensity - min value position | Decimal number |
| 10 | pcm_loudness_sma_amean | The normalized intensity - mean | Decimal number |
| 11 | pcm_loudness_sma_stddev | The normalized intensity - standard deviation | Decimal number |
| 12 | jitterLocal_sma_maxPos | Local Jitter: frame-to-frame jitter (pitch period length deviations) - max value position | Decimal number |
| 13 | jitterLocal_sma_minPos | Local Jitter: frame-to-frame jitter (pitch period length deviations) - min value position | Decimal number |
| 14 | jitterLocal_sma_amean | Local Jitter: frame-to-frame jitter (pitch period length deviations) - mean | Decimal number |
| 15 | jitterLocal_sma_stddev | Local Jitter: frame-to-frame jitter (pitch period length deviations) - standard deviation | Decimal number |
| 16 | jitterDDP_sma_maxPos | DDP Jitter: Differential frame-to-frame jitter (the ’jitter of the jitter’) - max value position | Decimal number |
| 17 | jitterDDP_sma_minPos | DDP Jitter: Differential frame-to-frame jitter (the ’jitter of the jitter’) - min value position | Decimal number |
| 18 | jitterDDP_sma_amean | DDP Jitter: Differential frame-to-frame jitter (the ’jitter of the jitter’) - mean | Decimal number |
| 19 | jitterDDP_sma_stddev | DDP Jitter: Differential frame-to-frame jitter (the ’jitter of the jitter’) - standard deviation | Decimal number |
| 20 | shimmerLocal_sma_maxPos | Shimmer : (amplitude deviations between pitch periods) - max value position | Decimal number |
| 21 | shimmerLocal_sma_minPos | Shimmer : (amplitude deviations between pitch periods) - min value position | Decimal number |
| 22 | shimmerLocal_sma_amean | Shimmer : (amplitude deviations between pitch periods) - mean | Decimal number |
| 23 | shimmerLocal_sma_stddev | Shimmer : (amplitude deviations between pitch periods) - standard deviation | Decimal number |
| 24 | F0final__Turn_numOnsets | The - mean | Decimal number |
| 25 | F0final__Turn_duration | The - mean | Decimal number |

[Regresar al Índice](#índice)

## NLP

| N° | Feature | Description | Values
| --- | --- | --- | --- |
| 1 | id_analysis | Unique identifier of the analysis | String text |
| 2 | start | Start time of the audio segment. | Decimal number (Greater than 0) |
| 3 | end | End time of the audio segment. | Decimal number (Greater than 0) |
| 4 | active_voice | Indicates the user to whom the intervention corresponding to the audio segment is assigned. | Decimal number (range 1 to 6) |
| 5 | frase | Provides automatic transcription of the corresponding sentence from the audio segment. | String text |
| 6 | data | Unpack sentences between their words. For each word you determine Adjective, Adverb, Interjection, Noun, Verb, Opposition. Auxiliary, etc. | json structure |

[Regresar al Índice](#índice)

## Head Sight

| N° | Feature | Description | Values
| --- | --- | --- | --- |
| 1 | id_analysis | Unique identifier of the analysis. | String text |
| 2 | start | start time of the video frame. | Decimal number (Greater than 0) |
| 3 | end | End time of the video frame. | Decimal number (Greater than 0) |
| 4 | position | Video frame number. | Decimal number (Greater than 0) |
| 5 | 1 | Indicates if user 1 is detected. | Booleano |
| 6 | 2 | Indicates if user 2 is detected. | Booleano |
| 7 | 3 | Indicates if user 3 is detected. | Booleano |
| 8 | 4 | Indicates if user 4 is detected. | Booleano |
| 9 | 5 | Indicates if user 5 is detected. | Booleano |
| 10 | 6 | Indicates if user 6 is detected. | Booleano |
| 11 | 1-x | Horizontal distance in the video where the user's face is located 1. | Integer |
| 12 | 1-y | Vertical distance in the video where the user's face is located 1. | Integer |
| 13 | 1-w | Width of user face 1. | Integer |
| 14 | 1-h | Height of user face 1. | Integer |
| 15 | 1-is_confirmed | Indicates whether the tracking of user 1's face movement is confirmed. | Booleano |
| 16 | 1-is_tentative | Indicates whether the tracking of user 1's face movement is tentative. | Booleano |
| 17 | 1-distance | Distance between the direction of the user's face 1 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 18 | 1-user_min_distance | User with smaller distance to the face direction of user 1.  | Decimal number (range 1 to 6)
| 19 | 2-x | Horizontal distance in the video where the user's face is located 2. | Integer |
| 20 | 2-y | Vertical distance in the video where the user's face is located 2. | Integer |
| 21 | 2-w | Width of user face 2. | Integer |
| 22 | 2-h | Height of user face 2. | Integer |
| 23 | 2-is_confirmed | Indicates whether the tracking of user 2's face movement is confirmed. | Booleano |
| 24 | 2-is_tentative | Indicates whether the tracking of user 2's face movement is tentative. | Booleano |
| 25 | 2-distance | Distance between the direction of the user's face 2 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 26 | 2-user_min_distance | User with smaller distance to the face direction of user 2. |  Decimal number (range 1 to 6) |
| 27 | 3-x | Horizontal distance in the video where the user's face is located 3. | Integer |
| 28 | 3-y | Vertical distance in the video where the user's face is located 3. | Integer |
| 29 | 3-w | Width of user face 3. | Integer |
| 30 | 3-h | Height of user face 3. | Integer |
| 31 | 3-is_confirmed | Indicates whether the tracking of user 3's face movement is confirmed. | Booleano |
| 32 | 3-is_tentative | Indicates whether the tracking of user 3's face movement is tentative. | Booleano |
| 33 | 3-distance | Distance between the direction of the user's face 3 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 34 | 3-user_min_distance | User with smaller distance to the face direction of user 3. | Decimal number (range 1 to 6) |
| 35 | 4-x | Horizontal distance in the video where the user's face is located 4. | Integer |
| 36 | 4-y | Vertical distance in the video where the user's face is located 4. | Integer |
| 37 | 4-w | Width of user face 4. | Integer |
| 38 | 4-h | Height of user face 4. | Integer |
| 39 | 4-is_confirmed | Indicates whether the tracking of user 4's face movement is confirmed. | Booleano |
| 40 | 4-is_tentative | Indicates whether the tracking of user 4's face movement is tentative. | Booleano |
| 41 | 4-distance | Distance between the direction of the user's face 4 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 42 | 4-user_min_distance | User with smaller distance to the face direction of user 4. | Decimal number (range 1 to 6) |
| 43 | 5-x | Horizontal distance in the video where the user's face is located 5. | Integer |
| 44 | 5-y | Vertical distance in the video where the user's face is located 5. | Integer |
| 45 | 5-w | Width of user face 5. | Integer |
| 46 | 5-h | Height of user face 5. | Integer |
| 47 | 5-is_confirmed | Indicates whether the tracking of user 5's face movement is confirmed. | Booleano |
| 48 | 5-is_tentative | Indicates whether the tracking of user 5's face movement is tentative. | Booleano |
| 49 | 5-distance | Distance between the direction of the user's face 5 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 50 | 5-user_min_distance | User with smaller distance to the face direction of user 5. | Decimal number (range 1 to 6) |
| 51 | 6-x | Horizontal distance in the video where the user's face is located 6. | Integer |
| 52 | 6-y | Vertical distance in the video where the user's face is located 6. | Integer |
| 53 | 6-w | Width of user face 6. | Integer |
| 54 | 6-h | Height of user face 6. | Integer |
| 55 | 6-is_confirmed | Indicates whether the tracking of user 6's face movement is confirmed. | Booleano |
| 66 | 6-is_tentative | Indicates whether the tracking of user 6's face movement is tentative. | Booleano |
| 57 | 6-distance | Distance between the direction of the user's face 6 to the user with minimum distance, from the perspective of the camera. | Decimal number (Greater than 0) |
| 58 | 6-user_min_distance | User with smaller distance to the face direction of user 6. | Decimal number (range 1 to 6) |

[Regresar al Índice](#índice)