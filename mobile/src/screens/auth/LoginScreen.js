import React, { useState } from 'react';
import { ActivityIndicator, Alert, Button, StyleSheet, Text, TextInput, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';
import api, { saveTokens } from '../../services/api';

const getErrorMessage = (error, fallbackMessage) => {
  if (error?.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (typeof error?.response?.data === 'string') {
    return error.response.data;
  }
  return fallbackMessage;
};

export default function LoginScreen({ navigation, route }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const successMessage = route?.params?.successMessage;

  const handleLogin = async () => {
    if (loading) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await api.post('/auth/token/', {
        username,
        password,
      });
      await saveTokens(response.data);
      navigation.replace('Main');
    } catch (err) {
      const message = getErrorMessage(err, 'Impossible de se connecter. Vérifiez vos identifiants.');
      setError(message);
      Alert.alert('Connexion échouée', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScreenContainer
      title="Bienvenue sur Check-IA"
      description="Connectez-vous pour accéder aux vérifications, analyses média et historique personnalisé."
    >
      <View style={styles.card}>
        {successMessage ? <Text style={styles.success}>{successMessage}</Text> : null}
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Text style={styles.label}>Nom d'utilisateur</Text>
        <TextInput
          style={styles.input}
          placeholder="ex: ibrahko"
          autoCapitalize="none"
          value={username}
          onChangeText={setUsername}
          editable={!loading}
        />
        <Text style={styles.label}>Mot de passe</Text>
        <TextInput
          style={styles.input}
          placeholder="••••••••"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
          editable={!loading}
        />
        {loading ? <ActivityIndicator size="small" color="#1D3557" /> : null}
        <Button title="Se connecter" onPress={handleLogin} disabled={loading} />
      </View>
      <Button title="Créer un compte" onPress={() => navigation.navigate('Register')} disabled={loading} />
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
  error: {
    color: '#D90429',
    marginBottom: 8,
  },
  success: {
    color: '#2A9D8F',
    marginBottom: 8,
  },
});
