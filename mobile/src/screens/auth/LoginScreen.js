import React from 'react';
import { Button, View } from 'react-native';

import ScreenContainer from '../../components/ScreenContainer';

export default function LoginScreen({ navigation }) {
  return (
    <View style={{ flex: 1 }}>
      <ScreenContainer
        title="Bienvenue sur Check-IA"
        description="Connectez-vous pour commencer la vérification de faits alimentée par l'IA."
      />
      <Button title="Créer un compte" onPress={() => navigation.navigate('Register')} />
    </View>
  );
}
