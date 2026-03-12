import * as ImagePicker from 'expo-image-picker';
import React, { useState } from 'react';
import { Alert, Button, StyleSheet, Text, TextInput, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';
import api from '../../services/api';

export default function ScanScreen() {
  const [textContent, setTextContent] = useState('');
  const [selectedAsset, setSelectedAsset] = useState(null);

  const pickMedia = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Permission requise', 'Autorisez la galerie pour sélectionner un média.');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      quality: 0.8,
    });

    if (!result.canceled) {
      setSelectedAsset(result.assets[0]);
    }
  };

  const uploadMedia = async () => {
    if (!selectedAsset) {
      Alert.alert('Aucun fichier', 'Sélectionnez une image ou vidéo avant envoi.');
      return;
    }

    const mediaType = selectedAsset.type === 'video' ? 'video' : 'image';

    try {
      const factResponse = await api.post('/facts/create/', {
        title: `Scan ${new Date().toISOString()}`,
        raw_input: textContent || 'Analyse média',
        source_url: '',
        content_type: mediaType,
        is_public: false,
      });

      const formData = new FormData();
      formData.append('fact_check', String(factResponse.data.id));
      formData.append('media_type', mediaType);
      formData.append('file', {
        uri: selectedAsset.uri,
        name: selectedAsset.fileName || `upload.${mediaType === 'video' ? 'mp4' : 'jpg'}`,
        type: selectedAsset.mimeType || (mediaType === 'video' ? 'video/mp4' : 'image/jpeg'),
      });

      await api.post('/media/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      Alert.alert('Succès', 'Média envoyé pour analyse IA.');
      setSelectedAsset(null);
      setTextContent('');
    } catch (error) {
      Alert.alert('Erreur', "Impossible d'envoyer le média pour le moment.");
    }
  };

  return (
    <ScreenContainer
      title="Scan"
      description="Soumettez un texte, une URL ou un média pour lancer une vérification assistée IA."
    >
      <View style={styles.card}>
        <Text style={styles.label}>Texte ou contexte</Text>
        <TextInput
          multiline
          numberOfLines={4}
          style={[styles.input, styles.textArea]}
          value={textContent}
          onChangeText={setTextContent}
          placeholder="Collez ici une affirmation, un lien ou un contexte à vérifier"
        />
        <Button title="Choisir image/vidéo" onPress={pickMedia} />
        {selectedAsset ? <Text style={styles.assetName}>Sélectionné: {selectedAsset.fileName || selectedAsset.uri}</Text> : null}
        <Button title="Uploader vers Check-IA" onPress={uploadMedia} />
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    gap: 10,
  },
  label: {
    fontWeight: '600',
    color: '#1D3557',
  },
  input: {
    borderWidth: 1,
    borderColor: '#DDE3EA',
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: '#FAFCFF',
  },
  textArea: {
    textAlignVertical: 'top',
    minHeight: 100,
  },
  assetName: {
    color: '#457B9D',
    fontSize: 12,
  },
});
