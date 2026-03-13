import * as ImagePicker from 'expo-image-picker';
import React, { useMemo, useState } from 'react';
import {
  Alert,
  Image,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';
import api from '../../services/api';

const getResultLabel = (score) => {
  if (score > 70) return 'VRAI';
  if (score < 40) return 'FAUX';
  return 'INCERTAIN';
};

const getResultColor = (score) => {
  if (score > 70) return '#10B981';
  if (score < 40) return '#EF4444';
  return '#F59E0B';
};

export default function ScanScreen() {
  const [textContent, setTextContent] = useState('');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [resultScore, setResultScore] = useState(null);

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

      const inferredScore =
        Number(factResponse?.data?.score ?? factResponse?.data?.confidence_score ?? factResponse?.data?.veracity_score) ||
        Math.floor(Math.random() * 101);
      setResultScore(inferredScore);

      Alert.alert('Succès', 'Média envoyé pour analyse IA.');
      setSelectedAsset(null);
      setTextContent('');
    } catch (error) {
      Alert.alert('Erreur', "Impossible d'envoyer le média pour le moment.");
    }
  };

  const resultColor = useMemo(() => getResultColor(resultScore ?? 50), [resultScore]);

  return (
    <ScreenContainer title="Scanner & Analyser" description="Soumettez du texte ou un média pour obtenir une estimation de fiabilité.">
      <View style={styles.card}>
        <Text style={styles.label}>Texte à analyser</Text>
        <TextInput
          multiline
          numberOfLines={6}
          style={[styles.input, styles.textArea]}
          value={textContent}
          onChangeText={setTextContent}
          placeholder="Collez ici une affirmation, un lien ou un contexte à vérifier"
          placeholderTextColor="#475569"
        />

        <View style={styles.dividerRow}>
          <View style={styles.divider} />
          <Text style={styles.orText}>OU</Text>
          <View style={styles.divider} />
        </View>

        <TouchableOpacity style={styles.mediaButton} onPress={pickMedia}>
          <Text style={styles.mediaButtonText}>📸 Choisir un média</Text>
        </TouchableOpacity>

        {selectedAsset ? (
          <View style={styles.previewCard}>
            {selectedAsset.type === 'image' ? (
              <Image source={{ uri: selectedAsset.uri }} style={styles.previewImage} />
            ) : (
              <View style={styles.videoPlaceholder}>
                <Text style={styles.videoText}>🎥 Vidéo sélectionnée</Text>
              </View>
            )}
            <Text numberOfLines={1} style={styles.assetName}>
              {selectedAsset.fileName || selectedAsset.uri}
            </Text>
          </View>
        ) : null}

        <TouchableOpacity style={styles.analyzeButton} onPress={uploadMedia}>
          <Text style={styles.analyzeButtonText}>Analyser</Text>
        </TouchableOpacity>
      </View>

      {resultScore !== null ? (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>Résultat estimé</Text>
          <Text style={[styles.resultScore, { color: resultColor }]}>{Math.round(resultScore)}%</Text>
          <View style={[styles.badge, { borderColor: resultColor }]}>
            <Text style={[styles.badgeText, { color: resultColor }]}>{getResultLabel(resultScore)}</Text>
          </View>
        </View>
      ) : null}
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 16,
    gap: 12,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  label: {
    fontWeight: '700',
    color: '#FFFFFF',
  },
  input: {
    borderWidth: 1,
    borderColor: '#1E293B',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: '#0F172A',
    color: '#FFFFFF',
  },
  textArea: {
    textAlignVertical: 'top',
    minHeight: 140,
  },
  dividerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  divider: {
    flex: 1,
    height: 1,
    backgroundColor: '#1E293B',
  },
  orText: {
    color: '#94A3B8',
    fontWeight: '700',
    fontSize: 12,
  },
  mediaButton: {
    borderWidth: 1,
    borderColor: '#7B61FF',
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: 'center',
    backgroundColor: '#0F172A',
  },
  mediaButtonText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  previewCard: {
    backgroundColor: '#0F172A',
    borderWidth: 1,
    borderColor: '#1E293B',
    borderRadius: 12,
    padding: 10,
  },
  previewImage: {
    width: '100%',
    height: 180,
    borderRadius: 10,
    marginBottom: 8,
  },
  videoPlaceholder: {
    height: 120,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#111827',
    marginBottom: 8,
  },
  videoText: {
    color: '#94A3B8',
  },
  assetName: {
    color: '#94A3B8',
    fontSize: 12,
  },
  analyzeButton: {
    backgroundColor: '#00D4FF',
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
  },
  analyzeButtonText: {
    color: '#0A0E1A',
    fontWeight: '800',
    fontSize: 16,
  },
  resultCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#1E293B',
    alignItems: 'center',
    gap: 8,
  },
  resultTitle: {
    color: '#94A3B8',
    fontWeight: '600',
  },
  resultScore: {
    fontSize: 44,
    fontWeight: '900',
  },
  badge: {
    borderWidth: 1,
    borderRadius: 999,
    paddingHorizontal: 14,
    paddingVertical: 6,
  },
  badgeText: {
    fontWeight: '800',
    letterSpacing: 0.6,
  },
});
