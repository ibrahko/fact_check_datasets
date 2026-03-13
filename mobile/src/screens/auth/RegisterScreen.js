import React, { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import api from '../../services/api';

const getErrorMessage = (error, fallbackMessage) => {
  if (error?.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (typeof error?.response?.data === 'string') {
    return error.response.data;
  }
  return fallbackMessage;
};

export default function RegisterScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [focusedField, setFocusedField] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleRegister = async () => {
    if (loading) return;
    setLoading(true);
    setError('');
    const payload = { username, email, password };
    try {
      await api.post('/auth/register/', payload, {
        headers: { 'Content-Type': 'application/json' },
      });
      navigation.navigate('Login', {
        successMessage: 'Compte créé avec succès. Connectez-vous pour continuer.',
      });
    } catch (err) {
      const message = getErrorMessage(err, 'Impossible de créer le compte pour le moment.');
      setError(message);
      Alert.alert('Inscription échouée', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.screen}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
        <View style={styles.header}>
          <Text style={styles.logoIcon}>🛡️</Text>
          <Text style={styles.title}>Rejoindre Check-IA</Text>
          <Text style={styles.subtitle}>Votre bouclier IA contre la désinformation.</Text>
        </View>

        <View style={styles.card}>
          <View style={styles.feedbackContainer}>
            {error ? <Text style={styles.error}>{error}</Text> : null}
          </View>

          <Text style={styles.label}>Nom d'utilisateur</Text>
          <TextInput
            style={[styles.input, focusedField === 'username' && styles.inputFocused]}
            placeholder="Nom d'utilisateur"
            placeholderTextColor="#64748B"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
            onFocus={() => setFocusedField('username')}
            onBlur={() => setFocusedField(null)}
          />

          <Text style={styles.label}>Email</Text>
          <TextInput
            style={[styles.input, focusedField === 'email' && styles.inputFocused]}
            placeholder="Email"
            placeholderTextColor="#64748B"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            onFocus={() => setFocusedField('email')}
            onBlur={() => setFocusedField(null)}
          />

          <Text style={styles.label}>Mot de passe</Text>
          <View style={styles.passwordContainer}>
            <TextInput
              style={[styles.input, styles.passwordInput, focusedField === 'password' && styles.inputFocused]}
              placeholder="Mot de passe"
              placeholderTextColor="#64748B"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
              onFocus={() => setFocusedField('password')}
              onBlur={() => setFocusedField(null)}
            />
            <TouchableOpacity style={styles.passwordToggle} onPress={() => setShowPassword((prev) => !prev)}>
              <Text style={styles.passwordToggleText}>{showPassword ? '🙈' : '👁'}</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.primaryButton, loading && { opacity: 0.6 }]}
            onPress={handleRegister}
            disabled={loading}
          >
            {loading ? <ActivityIndicator color="#0A0E1A" /> : null}
            <Text style={styles.primaryButtonText}>Créer mon compte</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => navigation.navigate('Login')} disabled={loading}>
            <Text style={styles.loginLink}>Déjà un compte ? Se connecter</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#0A0E1A' },
  scrollContent: { paddingHorizontal: 20, paddingTop: 48, paddingBottom: 40 },
  header: { alignItems: 'center', marginBottom: 24 },
  logoIcon: { fontSize: 48, marginBottom: 8 },
  title: { color: '#00D4FF', fontSize: 31, fontWeight: '800' },
  subtitle: { color: '#94A3B8', marginTop: 8 },
  card: { backgroundColor: '#111827', borderRadius: 18, padding: 18, gap: 8, borderWidth: 1, borderColor: '#1E293B' },
  feedbackContainer: { minHeight: 24, justifyContent: 'center' },
  label: { fontWeight: '700', color: '#FFFFFF', marginTop: 6, marginBottom: 6 },
  input: { borderWidth: 1, borderColor: '#1E293B', borderRadius: 12, paddingHorizontal: 12, paddingVertical: 12, marginBottom: 4, backgroundColor: '#111827', color: '#FFFFFF' },
  inputFocused: { borderColor: '#00D4FF' },
  passwordContainer: { position: 'relative' },
  passwordInput: { paddingRight: 44 },
  passwordToggle: { position: 'absolute', right: 12, top: 11 },
  passwordToggleText: { color: '#FFFFFF', fontSize: 18 },
  error: { color: '#EF4444' },
  primaryButton: { marginTop: 12, backgroundColor: '#00D4FF', borderRadius: 14, paddingVertical: 14, alignItems: 'center', flexDirection: 'row', justifyContent: 'center', gap: 8 },
  primaryButtonText: { color: '#0A0E1A', fontSize: 16, fontWeight: '800' },
  loginLink: { color: '#00D4FF', textAlign: 'center', marginTop: 14, fontWeight: '600' },
});
