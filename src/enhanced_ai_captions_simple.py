import json
import random
from typing import Optional, Dict, List

class EnhancedAICaptionGenerator:
    """Enhanced AI caption generator for restaurant food photos with fallback functionality"""
    
    def __init__(self, api_key: str):
        self.ai_enabled = False
        self.client = None
        
        # Try to import and initialize OpenAI only if available
        try:
            if api_key and api_key != 'your-openai-api-key-here':
                import openai
                self.client = openai.OpenAI(api_key=api_key)
                self.ai_enabled = True
                print("OpenAI client initialized successfully")
            else:
                print("OpenAI API key not provided, using fallback captions")
        except ImportError:
            print("OpenAI library not available, using fallback captions")
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}")
        
        # Restaurant-specific hashtag collections
        self.food_hashtags = {
            'general': ['#foodie', '#delicious', '#yummy', '#foodlover', '#tasty', '#fresh', '#homemade'],
            'restaurant': ['#restaurant', '#dining', '#chef', '#kitchen', '#culinary', '#finedining', '#localfood'],
            'experience': ['#foodexperience', '#diningout', '#foodporn', '#instafood', '#foodstagram', '#platepresentation'],
            'quality': ['#freshingredients', '#qualityfood', '#artisanal', '#gourmet', '#authentic', '#seasonal'],
            'atmosphere': ['#cozy', '#ambiance', '#perfectmeal', '#foodandwine', '#datenight', '#familydining']
        }
        
        # Cuisine-specific hashtags
        self.cuisine_hashtags = {
            'italian': ['#italian', '#pasta', '#pizza', '#risotto', '#gelato', '#italianfood'],
            'mexican': ['#mexican', '#tacos', '#guacamole', '#salsa', '#mexicanfood', '#spicy'],
            'asian': ['#asian', '#sushi', '#ramen', '#stirfry', '#dumplings', '#asianfusion'],
            'american': ['#american', '#burger', '#bbq', '#steakhouse', '#comfort', '#classic'],
            'mediterranean': ['#mediterranean', '#hummus', '#olive', '#seafood', '#healthy', '#fresh'],
            'french': ['#french', '#croissant', '#wine', '#cheese', '#pastry', '#frenchcuisine']
        }
        
    def analyze_food_image(self, image_base64: str, restaurant_context: Dict = None) -> Dict:
        """Analyze food image using OpenAI Vision API or return default analysis"""
        if not self.ai_enabled or not self.client:
            return self._create_default_analysis()
            
        try:
            # Prepare the context prompt
            context_info = ""
            if restaurant_context:
                context_info = f"""
Restaurant Context:
- Name: {restaurant_context.get('name', 'Our Restaurant')}
- Cuisine: {restaurant_context.get('cuisine', 'International')}
- Style: {restaurant_context.get('style', 'Casual Dining')}
- Location: {restaurant_context.get('location', 'Local')}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""Analyze this food image and provide detailed information for social media caption generation.
{context_info}

Please identify:
1. Main dish/food items
2. Cooking style/preparation method
3. Visual appeal elements (colors, presentation, garnishes)
4. Estimated cuisine type
5. Dining context (casual, fine dining, etc.)
6. Key ingredients visible
7. Overall mood/atmosphere

Respond in JSON format with these fields:
- main_dish: string
- cuisine_type: string
- cooking_style: string
- visual_elements: array of strings
- ingredients: array of strings
- dining_context: string
- mood: string
- appeal_factors: array of strings"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = analysis_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    # Fallback if JSON parsing fails
                    analysis = self._create_fallback_analysis(analysis_text)
            except json.JSONDecodeError:
                analysis = self._create_fallback_analysis(analysis_text)
                
            return analysis
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return self._create_default_analysis()
    
    def _create_fallback_analysis(self, text: str) -> Dict:
        """Create fallback analysis from text response"""
        return {
            "main_dish": "Delicious dish",
            "cuisine_type": "international",
            "cooking_style": "expertly prepared",
            "visual_elements": ["beautifully plated", "colorful presentation"],
            "ingredients": ["fresh ingredients"],
            "dining_context": "restaurant dining",
            "mood": "appetizing",
            "appeal_factors": ["visual appeal", "fresh preparation"]
        }
    
    def _create_default_analysis(self) -> Dict:
        """Create default analysis when API fails"""
        return {
            "main_dish": "Chef's special",
            "cuisine_type": "gourmet",
            "cooking_style": "artfully crafted",
            "visual_elements": ["beautiful presentation", "vibrant colors"],
            "ingredients": ["premium ingredients"],
            "dining_context": "fine dining",
            "mood": "elegant",
            "appeal_factors": ["exceptional quality", "artistic plating"]
        }
    
    def generate_caption(self, image_analysis: Dict, restaurant_context: Dict = None, caption_style: str = "engaging") -> str:
        """Generate engaging social media caption based on image analysis"""
        
        main_dish = image_analysis.get('main_dish', 'our signature dish')
        cuisine_type = image_analysis.get('cuisine_type', 'international').lower()
        visual_elements = image_analysis.get('visual_elements', [])
        ingredients = image_analysis.get('ingredients', [])
        mood = image_analysis.get('mood', 'delicious')
        
        # Caption templates based on style
        templates = {
            'engaging': [
                f"🍽️ {main_dish.title()} - where {mood} meets perfection! {self._get_visual_description(visual_elements)} Made with {self._format_ingredients(ingredients)}.",
                f"✨ Presenting our {main_dish}! {self._get_appeal_description(image_analysis)} Every bite is a celebration of flavor.",
                f"👨‍🍳 Chef's masterpiece: {main_dish}! {self._get_visual_description(visual_elements)} Crafted with passion and {self._format_ingredients(ingredients)}.",
                f"🌟 {main_dish.title()} that speaks to your soul! {self._get_mood_description(mood)} {self._get_visual_description(visual_elements)}"
            ],
            'professional': [
                f"Expertly crafted {main_dish} featuring {self._format_ingredients(ingredients)}. {self._get_visual_description(visual_elements)}",
                f"Our signature {main_dish} - a testament to culinary excellence. {self._get_appeal_description(image_analysis)}",
                f"Artisanal {main_dish} prepared with meticulous attention to detail. {self._get_visual_description(visual_elements)}"
            ],
            'casual': [
                f"😋 {main_dish.title()} looking absolutely amazing! {self._get_visual_description(visual_elements)}",
                f"🤤 Can't get enough of this {main_dish}! {self._get_mood_description(mood)}",
                f"📸 Had to share this gorgeous {main_dish}! {self._get_visual_description(visual_elements)}"
            ]
        }
        
        # Select random template
        template = random.choice(templates.get(caption_style, templates['engaging']))
        
        # Add restaurant context if available
        if restaurant_context and restaurant_context.get('name'):
            template += f" Visit us at {restaurant_context['name']}!"
        
        # Add relevant hashtags
        hashtags = self._generate_hashtags(cuisine_type, image_analysis, restaurant_context)
        
        return f"{template}\n\n{hashtags}"
    
    def _get_visual_description(self, visual_elements: List[str]) -> str:
        """Create description from visual elements"""
        if not visual_elements:
            return "Beautifully presented with artistic flair."
        
        if len(visual_elements) == 1:
            return f"Notice the {visual_elements[0]}."
        elif len(visual_elements) == 2:
            return f"Love the {visual_elements[0]} and {visual_elements[1]}."
        else:
            return f"Featuring {', '.join(visual_elements[:-1])}, and {visual_elements[-1]}."
    
    def _get_appeal_description(self, analysis: Dict) -> str:
        """Create description from appeal factors"""
        appeal_factors = analysis.get('appeal_factors', [])
        if appeal_factors:
            return f"Showcasing {', '.join(appeal_factors[:2])}."
        return "A true feast for the senses."
    
    def _get_mood_description(self, mood: str) -> str:
        """Create mood-based description"""
        mood_descriptions = {
            'elegant': 'Sophisticated and refined.',
            'appetizing': 'Making mouths water everywhere!',
            'cozy': 'Perfect comfort food vibes.',
            'vibrant': 'Bursting with color and life!',
            'rustic': 'Authentic and hearty goodness.',
            'delicious': 'Pure culinary bliss!'
        }
        return mood_descriptions.get(mood.lower(), 'Absolutely irresistible!')
    
    def _format_ingredients(self, ingredients: List[str]) -> str:
        """Format ingredients list for caption"""
        if not ingredients:
            return "the finest ingredients"
        
        if len(ingredients) == 1:
            return ingredients[0]
        elif len(ingredients) == 2:
            return f"{ingredients[0]} and {ingredients[1]}"
        else:
            return f"{', '.join(ingredients[:-1])}, and {ingredients[-1]}"
    
    def _generate_hashtags(self, cuisine_type: str, analysis: Dict, restaurant_context: Dict = None) -> str:
        """Generate relevant hashtags based on analysis"""
        hashtags = []
        
        # Add general food hashtags
        hashtags.extend(random.sample(self.food_hashtags['general'], 3))
        
        # Add restaurant hashtags
        hashtags.extend(random.sample(self.food_hashtags['restaurant'], 2))
        
        # Add cuisine-specific hashtags
        if cuisine_type in self.cuisine_hashtags:
            hashtags.extend(random.sample(self.cuisine_hashtags[cuisine_type], 2))
        
        # Add experience hashtags
        hashtags.extend(random.sample(self.food_hashtags['experience'], 2))
        
        # Add quality hashtags
        hashtags.extend(random.sample(self.food_hashtags['quality'], 2))
        
        # Add restaurant-specific hashtags if available
        if restaurant_context:
            if restaurant_context.get('name'):
                # Create restaurant hashtag
                restaurant_tag = f"#{restaurant_context['name'].replace(' ', '').lower()}"
                hashtags.append(restaurant_tag)
            
            if restaurant_context.get('location'):
                location_tag = f"#{restaurant_context['location'].replace(' ', '').lower()}food"
                hashtags.append(location_tag)
        
        # Remove duplicates and limit to 15 hashtags
        unique_hashtags = list(dict.fromkeys(hashtags))[:15]
        
        return ' '.join(unique_hashtags)
    
    def generate_caption_from_image(self, image_base64: str, restaurant_context: Dict = None, caption_style: str = "engaging") -> str:
        """Complete pipeline: analyze image and generate caption"""
        try:
            # Analyze the image
            analysis = self.analyze_food_image(image_base64, restaurant_context)
            
            # Generate caption
            caption = self.generate_caption(analysis, restaurant_context, caption_style)
            
            return caption
            
        except Exception as e:
            print(f"Error generating caption: {e}")
            # Return fallback caption
            return self._generate_fallback_caption(restaurant_context)
    
    def _generate_fallback_caption(self, restaurant_context: Dict = None) -> str:
        """Generate fallback caption when AI fails"""
        fallback_captions = [
            "🍽️ Fresh from our kitchen to your table! Every bite tells a story of passion and flavor. #FreshFood #RestaurantLife #Foodie #Delicious #ChefSpecial #LocalDining",
            "👨‍🍳 Our chef's masterpiece is ready to delight your senses. Made with love and the finest ingredients! #ChefSpecial #FineDining #FoodArt #Gourmet #CulinaryExcellence #Handcrafted",
            "🌟 Today's special is more than just a meal - it's an experience! Come taste the difference quality makes. #TodaysSpecial #QualityFood #RestaurantExperience #Foodie #LocalFavorite #Delicious",
            "✨ Every dish is crafted with attention to detail and a sprinkle of culinary magic! #CraftedWithLove #CulinaryMagic #AttentionToDetail #FoodCraftsmanship #Restaurant #Gourmet"
        ]
        
        caption = random.choice(fallback_captions)
        
        if restaurant_context and restaurant_context.get('name'):
            caption += f" Visit us at {restaurant_context['name']}!"
        
        return caption
    
    def generate_ai_content(self, restaurant_context: Dict = None) -> str:
        """Generate AI content for restaurant posts"""
        if self.ai_enabled and self.client:
            try:
                # Create a prompt for general restaurant content
                prompt = f"""Generate an engaging social media post for a restaurant with the following context:
Restaurant Name: {restaurant_context.get('name', 'Our Restaurant')}
Cuisine Type: {restaurant_context.get('cuisine', 'International')}
Location: {restaurant_context.get('location', 'Local')}

Create a post that could be about:
- Daily specials or menu highlights
- Restaurant atmosphere and experience
- Chef recommendations
- Customer appreciation
- Behind-the-scenes content
- Seasonal ingredients or dishes

Make it engaging, authentic, and include relevant hashtags. Keep it under 280 characters for optimal social media engagement."""

                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a social media expert specializing in restaurant marketing. Create engaging, authentic posts that drive customer engagement."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.8
                )
                
                content = response.choices[0].message.content.strip()
                
                # Add restaurant-specific hashtags
                hashtags = self._generate_hashtags(
                    restaurant_context.get('cuisine', 'international').lower(),
                    {'main_dish': 'restaurant content', 'cuisine_type': restaurant_context.get('cuisine', 'international')},
                    restaurant_context
                )
                
                # Combine content with hashtags if not already included
                if '#' not in content:
                    content += f"\n\n{hashtags}"
                
                return content
                
            except Exception as e:
                print(f"AI content generation failed: {e}")
        
        # Fallback content
        fallback_suggestions = [
            "🍽️ Fresh ingredients, amazing flavors! Come taste the difference at our restaurant. #FreshFood #LocalDining #RestaurantLife #Foodie #ChefSpecial",
            "👨‍🍳 Our chef's special creations are waiting for you. Book your table today! #ChefSpecial #FineDining #Foodie #CulinaryArt #RestaurantExperience",
            "🌟 Thank you to all our amazing customers! Your support means everything to us. #Grateful #Community #Restaurant #CustomerLove #LocalSupport",
            "🥘 New menu items just dropped! Our latest creations are ready to delight your taste buds. #NewMenu #Innovation #Delicious #FoodieAlert #TasteBuds",
            "📸 Behind the scenes in our kitchen - where the magic happens! #BehindTheScenes #Kitchen #Passion #CulinaryMagic #ChefLife",
            "🎉 Weekend special: Join us for an unforgettable dining experience! #WeekendSpecial #Dining #Experience #RestaurantLife #SpecialOffer"
        ]
        
        content = random.choice(fallback_suggestions)
        
        if restaurant_context and restaurant_context.get('name'):
            content += f" Visit us at {restaurant_context['name']}!"
        
        return content

