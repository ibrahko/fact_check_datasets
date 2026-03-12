import React from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function ProfileScreen({ navigation }) {
  return (
    <ScreenContainer title="Profil" description="Gestion du compte et préférences de vérification.">
      <View style={styles.card}>
        <Text style={styles.name}>Utilisateur Demo</Text>
        <Text style={styles.email}>demo@check-ia.app</Text>
      </View>
      <Button title="Se déconnecter" onPress={() => navigation.replace('Auth')} />
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    gap: 6,
  },
  name: {
    fontSize: 18,
    color: '#1D3557',
    fontWeight: '700',
  },
  email: {
    color: '#457B9D',
  },
});
