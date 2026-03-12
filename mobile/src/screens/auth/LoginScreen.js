import React from 'react';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function LoginScreen({ navigation }) {
  return (
    <ScreenContainer
      title="Bienvenue sur Check-IA"
      description="Connectez-vous pour accéder aux vérifications, analyses média et historique personnalisé."
    >
      <View style={styles.card}>
        <Text style={styles.label}>Nom d'utilisateur</Text>
        <TextInput style={styles.input} placeholder="ex: ibrahko" autoCapitalize="none" />
        <Text style={styles.label}>Mot de passe</Text>
        <TextInput style={styles.input} placeholder="••••••••" secureTextEntry />
        <Button title="Se connecter" onPress={() => navigation.replace('Main')} />
      </View>
      <Button title="Créer un compte" onPress={() => navigation.navigate('Register')} />
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
