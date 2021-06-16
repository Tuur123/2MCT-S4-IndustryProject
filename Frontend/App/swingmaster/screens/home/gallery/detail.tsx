import React, { useState } from 'react';
import {
  Text,
  View,
  Image,
  TouchableOpacity,
  Alert,
  Modal,
  Dimensions,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as MediaLibrary from 'expo-media-library';
import { Video, AVPlaybackStatus } from 'expo-av';

import { accent, neutral } from '../../../styles/colors/colors';
import Play from '../../../assets/icons/play';
import { inputs } from '../../../styles/components/Inputs';
import BackArrow from '../../../assets/icons/backarrow';

const Detail = ({ route, navigation }: any) => {
  const [isVideoPlayer, setIsVideoPlayer] = useState<boolean>(false);
  const [status, setStatus] = React.useState({});
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const videoPlayer = React.useRef(null);
  const video = route.params.video;
  const tumbnail = route.params.tumbnail;
  let filename = video.filename.replace('.mp4', '');
  if (filename.length > 25) {
    filename = `${filename.slice(0, 25)}...`;
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: neutral[900] }}>
      <Modal
        animationType="fade"
        transparent={true}
        visible={isVideoPlayer}
        onRequestClose={() => {
          Alert.alert('Modal has been closed.');
        }}
      >
        <View style={{}}>
          <View style={{ backgroundColor: neutral[900] }}>
            <Video
              ref={videoPlayer}
              style={{
                height: Dimensions.get('window').height - 75,
                width: Dimensions.get('window').width,
              }}
              source={{
                uri: video.uri,
              }}
              shouldPlay={true}
              useNativeControls
              resizeMode="contain"
              onPlaybackStatusUpdate={(status) => setStatus(() => status)}
            />

            <TouchableOpacity
              style={{
                backgroundColor: accent[400],
                height: 75,
                justifyContent: 'center',
                alignItems: 'center',
              }}
              onPress={() => {
                setIsVideoPlayer(!isVideoPlayer);
              }}
            >
              <Text
                style={{
                  textAlign: 'center',
                  fontSize: 20,
                  fontWeight: 'bold',
                }}
              >
                close videoplayer
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
      <TouchableOpacity
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: neutral[800],
        }}
        onPress={() => {
          setIsVideoPlayer(true);
        }}
      >
        <Image
          source={{ uri: tumbnail }}
          style={{ width: '100%', height: 300, opacity: 0.4 }}
        />
        <View style={{ position: 'absolute' }}>
          <Play />
        </View>
      </TouchableOpacity>
      <TouchableOpacity
        style={{
          position: 'absolute',
          top: 50,
          left: 30,
          width: 17,
          height: 33,
        }}
        onPress={() => {
          navigation.goBack();
        }}
      >
        <BackArrow color={neutral[200]} />
      </TouchableOpacity>
      <View style={{ flex: 1, backgroundColor: neutral[200] }}>
        <Text style={{ textAlign: 'center', fontSize: 20, marginVertical: 20 }}>
          {filename}
        </Text>
        <View style={{ justifyContent: 'flex-end' }}>
          <TouchableOpacity
            style={inputs.buttonWhite}
            disabled={isUploading}
            onPress={async () => {
              setIsUploading(true);
              let form_data = new FormData();
              form_data.append('video', video.uri, video.filename);

              // ip veranderen naar ip van pc, smartphone moet ook op zelfde netwerk zitten
              fetch('http://10.2.167.3:5000/upload', {
                method: 'POST',
                headers: {
                  Accept: 'multipart/form-data',
                  'Content-Type': 'multipart/form-data',
                },
                body: video,
              })
                .then((response) => response.json())
                .then((success) => {
                  console.log(success);
                  setIsUploading(false);
                })
                .catch((error) => {
                  console.error(error);
                  setIsUploading(false);
                  Alert.alert(`Failed to upload`, ``, [
                    {
                      text: 'Ok',
                      onPress: () => {},
                      style: 'default',
                    },
                  ]);
                });
            }}
          >
            {isUploading ? (
              <ActivityIndicator size="small" color={neutral[900]} />
            ) : (
              <Text style={inputs.buttonText}>Analyze video</Text>
            )}
          </TouchableOpacity>
          <TouchableOpacity
            style={inputs.buttonWhite}
            onPress={async () => {
              const album = await MediaLibrary.getAlbumAsync('swingmaster');
              const res = await MediaLibrary.removeAssetsFromAlbumAsync(
                video,
                album
              );
              res
                ? navigation.goBack()
                : Alert.alert(`Failed to delete`, ``, [
                    {
                      text: 'Ok',
                      onPress: () => {},
                      style: 'default',
                    },
                  ]);
            }}
          >
            <Text style={[inputs.buttonText, inputs.error]}>Delete video</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default Detail;
