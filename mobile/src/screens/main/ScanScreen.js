import React from 'react';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function ScanScreen() {
  return (
    <ScreenContainer
      title="Scan"
      description="Soumettez un texte, une URL ou un média pour lancer une vérification assistée IA."
    >
      <View style={styles.card}>
        <Text style={styles.label}>Texte ou URL à analyser</Text>
        <TextInput
          multiline
          numberOfLines={4}
          style={[styles.input, styles.textArea]}
          placeholder="Collez ici une affirmation, un lien ou un contexte à vérifier"
        />
        <Button title="Lancer l'analyse" onPress={() => {}} />
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
});
