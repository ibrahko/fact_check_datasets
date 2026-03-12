import React from 'react';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function RegisterScreen({ navigation }) {
  return (
    <ScreenContainer
      title="Créer un compte"
      description="Inscription rapide pour démarrer vos analyses de fact-checking et deepfake."
    >
      <View style={styles.card}>
        <Text style={styles.label}>Nom d'utilisateur</Text>
        <TextInput style={styles.input} placeholder="Votre identifiant" autoCapitalize="none" />
        <Text style={styles.label}>Email</Text>
        <TextInput style={styles.input} placeholder="vous@email.com" keyboardType="email-address" autoCapitalize="none" />
        <Text style={styles.label}>Mot de passe</Text>
        <TextInput style={styles.input} placeholder="••••••••" secureTextEntry />
        <Button title="Créer mon compte" onPress={() => navigation.navigate('Login')} />
      </View>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    gap: 8,
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
    marginBottom: 8,
    backgroundColor: '#FAFCFF',
  },
});
