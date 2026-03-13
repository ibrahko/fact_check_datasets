import React, { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

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
  const [focusedField, setFocusedField] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

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
    <KeyboardAvoidingView
      style={styles.screen}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={styles.logoIcon}>🛡️</Text>
          <Text style={styles.logoText}>CHECK-IA</Text>
          <Text style={styles.subtitle}>Vérifiez. Analysez. Protégez.</Text>
          <Text style={styles.tagline}>Combattre la désinformation avec l'intelligence artificielle</Text>
        </View>

        <View style={styles.card}>
          <View style={styles.feedbackContainer}>
            {successMessage ? <Text style={styles.success}>{successMessage}</Text> : null}
            {error ? <Text style={styles.error}>{error}</Text> : null}
          </View>

          <Text style={styles.label}>Nom d'utilisateur</Text>
          <TextInput
            style={[styles.input, focusedField === 'username' && styles.inputFocused]}
            placeholder="ex: ibrahko"
            placeholderTextColor="#475569"
            autoCapitalize="none"
            value={username}
            onChangeText={setUsername}
            editable={!loading}
            onFocus={() => setFocusedField('username')}
            onBlur={() => setFocusedField(null)}
          />

          <Text style={styles.label}>Mot de passe</Text>
          <View style={styles.passwordContainer}>
            <TextInput
              style={[styles.input, styles.passwordInput, focusedField === 'password' && styles.inputFocused]}
              placeholder="••••••••"
              placeholderTextColor="#475569"
              secureTextEntry={!showPassword}
              value={password}
              onChangeText={setPassword}
              editable={!loading}
              onFocus={() => setFocusedField('password')}
              onBlur={() => setFocusedField(null)}
            />
            <Pressable style={styles.passwordToggle} onPress={() => setShowPassword((prev) => !prev)}>
              <Text style={styles.passwordToggleText}>{showPassword ? '🙈' : '👁'}</Text>
            </Pressable>
          </View>

          {loading ? <ActivityIndicator size="small" color="#00D4FF" /> : null}

          <TouchableOpacity style={styles.primaryButton} onPress={handleLogin} disabled={loading}>
            <Text style={styles.primaryButtonText}>Se connecter</Text>
          </TouchableOpacity>

          <Pressable style={styles.secondaryButton} onPress={() => navigation.navigate('Register')} disabled={loading}>
            <Text style={styles.secondaryButtonText}>Créer un compte</Text>
          </Pressable>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#0A0E1A',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 48,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  logoIcon: {
    fontSize: 56,
    marginBottom: 8,
  },
  logoText: {
    fontSize: 36,
    fontWeight: '900',
    color: '#00D4FF',
    letterSpacing: 1,
  },
  subtitle: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '700',
    marginTop: 6,
  },
  tagline: {
    marginTop: 10,
    textAlign: 'center',
    color: '#94A3B8',
    fontSize: 13,
    lineHeight: 20,
  },
  card: {
    backgroundColor: '#111827',
    borderRadius: 18,
    padding: 18,
    gap: 8,
    borderWidth: 1,
    borderColor: '#1E293B',
  },
  feedbackContainer: {
    minHeight: 24,
    justifyContent: 'center',
  },
  label: {
    fontWeight: '700',
    color: '#FFFFFF',
    marginTop: 6,
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: '#1E293B',
    borderRadius: 12,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 4,
    backgroundColor: '#111827',
    color: '#FFFFFF',
  },
  inputFocused: {
    borderColor: '#00D4FF',
  },
  passwordContainer: {
    position: 'relative',
  },
  passwordInput: {
    paddingRight: 44,
  },
  passwordToggle: {
    position: 'absolute',
    right: 12,
    top: 11,
  },
  passwordToggleText: {
    color: '#FFFFFF',
    fontSize: 18,
  },
  error: {
    color: '#EF4444',
  },
  success: {
    color: '#10B981',
  },
  primaryButton: {
    marginTop: 10,
    backgroundColor: '#00D4FF',
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#0A0E1A',
    fontSize: 16,
    fontWeight: '800',
  },
  secondaryButton: {
    marginTop: 10,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#00D4FF',
    paddingVertical: 13,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#00D4FF',
    fontWeight: '700',
  },
});
